"""
Azure OpenAI Client
Handles authentication and API calls to Azure OpenAI using Azure AD credentials
"""
import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta


class AzureOpenAIClient:
    """
    Client for Azure OpenAI API with Azure AD authentication
    """
    
    def __init__(self):
        """Initialize Azure OpenAI client with credentials from environment"""
        self.endpoint = os.getenv("OPENAI_ENDPOINT", "").rstrip('/')
        self.tenant_id = os.getenv("TENANT_ID", "")
        self.client_id = os.getenv("CLIENT_ID", "")
        self.client_secret = os.getenv("CLIENT_SECRET", "")
        self.token_url = os.getenv("TOKEN_URL", "")
        self.token_scope = os.getenv("TOKEN_SCOPE", "")
        self.deployment = os.getenv("OPENAI_DEPLOYMENT", "gpt-4")
        self.api_version = os.getenv("OPENAI_API_VERSION", "2024-02-15-preview")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
        
        # Detect if using newer model that requires max_completion_tokens
        # Models like gpt-5, o1, o3 use max_completion_tokens instead of max_tokens
        self.use_completion_tokens = self._should_use_completion_tokens()
        
        # Token management
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
        
        # Validate configuration
        self._validate_config()
    
    def _should_use_completion_tokens(self) -> bool:
        """
        Check if the model requires max_completion_tokens instead of max_tokens
        
        Returns:
            bool: True if model uses max_completion_tokens
        """
        # Newer models (gpt-5.x, o1, o3, etc.) require max_completion_tokens
        deployment_lower = self.deployment.lower()
        new_model_prefixes = ('gpt-5', 'o1', 'o3', 'gpt5')
        return any(deployment_lower.startswith(prefix) for prefix in new_model_prefixes)
    
    def _should_exclude_temperature(self) -> bool:
        """
        Check if the model doesn't support temperature parameter
        
        Returns:
            bool: True if temperature should be excluded
        """
        # Reasoning models (o1, o3) and newer models (gpt-5) don't support temperature
        deployment_lower = self.deployment.lower()
        no_temp_prefixes = ('gpt-5', 'o1', 'o3', 'gpt5')
        return any(deployment_lower.startswith(prefix) for prefix in no_temp_prefixes)
    
    def _validate_config(self):
        """Validate that required configuration is present"""
        required = {
            'OPENAI_ENDPOINT': self.endpoint,
            'TENANT_ID': self.tenant_id,
            'CLIENT_ID': self.client_id,
            'CLIENT_SECRET': self.client_secret,
            'TOKEN_URL': self.token_url,
            'TOKEN_SCOPE': self.token_scope
        }
        
        missing = [key for key, value in required.items() if not value]
        
        if missing:
            raise ValueError(
                f"Missing required Azure OpenAI configuration: {', '.join(missing)}\n"
                "Please check your .env file and ensure all credentials are set."
            )
    
    def _get_access_token(self) -> str:
        """
        Get or refresh Azure AD access token
        
        Returns:
            str: Valid access token
        """
        # Check if we have a valid token
        if self._access_token and self._token_expiry:
            if datetime.now() < self._token_expiry - timedelta(minutes=5):
                return self._access_token
        
        # Request new token
        try:
            payload = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': self.token_scope
            }
            
            response = requests.post(self.token_url, data=payload)
            response.raise_for_status()
            
            token_data = response.json()
            self._access_token = token_data['access_token']
            
            # Set expiry (default to 1 hour if not provided)
            expires_in = token_data.get('expires_in', 3600)
            self._token_expiry = datetime.now() + timedelta(seconds=expires_in)
            
            return self._access_token
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to obtain Azure AD access token: {e}")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Create a chat completion
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (overrides default)
            max_tokens: Maximum tokens to generate (overrides default)
            stream: Whether to stream the response
            
        Returns:
            Dict: API response
        """
        token = self._get_access_token()
        
        url = (
            f"{self.endpoint}/openai/deployments/{self.deployment}/"
            f"chat/completions?api-version={self.api_version}"
        )
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Build payload with correct token parameter based on model
        tokens_value = max_tokens if max_tokens is not None else self.max_tokens
        
        payload = {
            'messages': messages,
            'stream': stream
        }
        
        # Add temperature only if model supports it
        if not self._should_exclude_temperature():
            if temperature is not None:
                payload['temperature'] = temperature
            elif self.temperature is not None:
                payload['temperature'] = self.temperature
        
        # Use correct token parameter based on model type
        if self.use_completion_tokens:
            payload['max_completion_tokens'] = tokens_value
        else:
            payload['max_tokens'] = tokens_value
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            # Provide more helpful error messages
            status_code = e.response.status_code if e.response else 'unknown'
            if status_code == 400:
                raise Exception(
                    f"Azure OpenAI API error (400): Bad Request. "
                    f"Check your deployment name '{self.deployment}' and API version."
                )
            elif status_code == 401:
                raise Exception(
                    "Azure OpenAI API error (401): Authentication failed. "
                    "Check your credentials (CLIENT_ID, CLIENT_SECRET, TENANT_ID)."
                )
            elif status_code == 404:
                raise Exception(
                    f"Azure OpenAI API error (404): Deployment '{self.deployment}' not found. "
                    "Verify the deployment name in Azure Portal."
                )
            elif status_code == 429:
                raise Exception(
                    "Azure OpenAI API error (429): Rate limit exceeded. "
                    "Please wait and try again."
                )
            else:
                raise Exception(f"Azure OpenAI API request failed: {e}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Azure OpenAI API request failed: {e}")
    
    def get_response_content(self, api_response: Dict[str, Any]) -> str:
        """
        Extract content from API response
        
        Args:
            api_response: API response dictionary
            
        Returns:
            str: Response content
        """
        try:
            content = api_response['choices'][0]['message']['content']
            # Handle None or empty content
            if content is None or content.strip() == '':
                # Check if there's a refusal or finish reason
                finish_reason = api_response['choices'][0].get('finish_reason', '')
                if finish_reason == 'content_filter':
                    return "I apologize, but I couldn't generate a response due to content filtering. Please try rephrasing your request."
                elif finish_reason == 'length':
                    return "My response was cut off due to length limits. Let me try to be more concise. Could you repeat your question?"
                return "I'm sorry, I couldn't generate a response. Please try again."
            return content
        except (KeyError, IndexError, TypeError) as e:
            raise Exception(f"Failed to extract content from API response: {e}")
    
    def create_system_message(self, content: str) -> Dict[str, str]:
        """
        Create a system message
        
        Args:
            content: Message content
            
        Returns:
            Dict: Message dictionary
        """
        return {'role': 'system', 'content': content}
    
    def create_user_message(self, content: str) -> Dict[str, str]:
        """
        Create a user message
        
        Args:
            content: Message content
            
        Returns:
            Dict: Message dictionary
        """
        return {'role': 'user', 'content': content}
    
    def create_assistant_message(self, content: str) -> Dict[str, str]:
        """
        Create an assistant message
        
        Args:
            content: Message content
            
        Returns:
            Dict: Message dictionary
        """
        return {'role': 'assistant', 'content': content}
    
    def test_connection(self) -> bool:
        """
        Test the Azure OpenAI connection
        
        Returns:
            bool: True if connection successful
        """
        try:
            messages = [
                self.create_system_message("You are a helpful assistant."),
                self.create_user_message("Say 'Connection successful!' if you can read this.")
            ]
            
            response = self.chat_completion(messages, max_tokens=50)
            content = self.get_response_content(response)
            
            return "successful" in content.lower()
            
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False


# Singleton instance
_client_instance: Optional[AzureOpenAIClient] = None


def get_openai_client() -> AzureOpenAIClient:
    """
    Get or create singleton Azure OpenAI client instance
    
    Returns:
        AzureOpenAIClient: Client instance
    """
    global _client_instance
    
    if _client_instance is None:
        _client_instance = AzureOpenAIClient()
    
    return _client_instance
