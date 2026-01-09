"""
A2A Protocol Test Client
Use this to test the Travel Agent A2A server locally

This client supports OAuth2 authentication (Client Credentials flow)
"""
import requests
import json
import uuid
import os
from typing import Optional


class A2ATestClient:
    """
    Simple A2A client for testing the Travel Agent
    
    Supports OAuth2 Client Credentials authentication
    """
    
    # Default OAuth2 credentials for development
    DEFAULT_CLIENT_ID = "travel-agent-client"
    DEFAULT_CLIENT_SECRET = "dev-secret-change-in-production-12345"
    DEFAULT_SCOPE = "a2a:travel-agent"
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        """
        Initialize the test client
        
        Args:
            base_url: The base URL of the A2A server
        """
        self.base_url = base_url.rstrip("/")
        self.context_id: Optional[str] = None
        self.task_id: Optional[str] = None
        self.access_token: Optional[str] = None
        
        # OAuth2 credentials from environment or defaults
        self.client_id = os.getenv("OAUTH2_CLIENT_ID", self.DEFAULT_CLIENT_ID)
        self.client_secret = os.getenv("OAUTH2_CLIENT_SECRET", self.DEFAULT_CLIENT_SECRET)
        self.scope = os.getenv("OAUTH2_SCOPE", self.DEFAULT_SCOPE)
    
    def authenticate(self) -> bool:
        """
        Obtain an OAuth2 access token using client credentials
        
        Returns:
            bool: True if authentication was successful
        """
        try:
            response = requests.post(
                f"{self.base_url}/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "scope": self.scope
                }
            )
            response.raise_for_status()
            result = response.json()
            self.access_token = result.get("access_token")
            return bool(self.access_token)
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def _get_auth_headers(self) -> dict:
        """Get authorization headers if token is available"""
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers
    
    def get_agent_card(self) -> dict:
        """
        Fetch the agent card from the well-known endpoint
        (No authentication required)
        
        Returns:
            dict: The agent card JSON
        """
        # Try new path first, then legacy path
        for path in ["/.well-known/agent-card.json", "/.well-known/agent.json"]:
            try:
                response = requests.get(f"{self.base_url}{path}")
                if response.status_code == 200:
                    return response.json()
            except:
                pass
        
        # If both fail, raise error
        response = requests.get(f"{self.base_url}/.well-known/agent-card.json")
        response.raise_for_status()
        return response.json()
    
    def send_message(self, message: str, new_context: bool = False) -> dict:
        """
        Send a message to the travel agent using A2A protocol
        (Requires authentication)
        
        Args:
            message: The message to send
            new_context: If True, start a new conversation context
            
        Returns:
            dict: The JSON-RPC response
        """
        # Ensure we have a token
        if not self.access_token:
            if not self.authenticate():
                raise Exception("Authentication required but failed")
        
        if new_context:
            self.context_id = str(uuid.uuid4())
            self.task_id = None  # New context means new task
        
        # Build the A2A JSON-RPC request
        request_body = {
            "role": "user",
            "messageId": str(uuid.uuid4()),
            "parts": [
                {
                    "kind": "text",
                    "text": message
                }
            ]
        }
        
        # Only include context_id if we have it (for conversation continuity)
        # Don't include task_id - each message creates a new task
        if self.context_id:
            request_body["contextId"] = self.context_id
        
        request = {
            "jsonrpc": "2.0",
            "method": "message/send",
            "id": str(uuid.uuid4()),
            "params": {
                "message": request_body
            }
        }
        
        response = requests.post(
            self.base_url,
            json=request,
            headers=self._get_auth_headers()
        )
        
        # Check for auth errors
        if response.status_code == 401:
            # Try to re-authenticate and retry once
            if self.authenticate():
                response = requests.post(
                    self.base_url,
                    json=request,
                    headers=self._get_auth_headers()
                )
        
        response.raise_for_status()
        result = response.json()
        
        # Store context_id and task_id from response for subsequent requests
        if "result" in result:
            res = result["result"]
            if "contextId" in res:
                self.context_id = res["contextId"]
            if "id" in res:
                self.task_id = res["id"]
        
        return result
    
    def extract_response_text(self, response: dict) -> str:
        """
        Extract the text response from an A2A response
        
        Args:
            response: The A2A JSON-RPC response
            
        Returns:
            str: The extracted text response
        """
        try:
            result = response.get("result", {})
            
            # Handle task response format
            if "status" in result:
                status = result.get("status", {})
                message = status.get("message", {})
            else:
                message = result.get("message", {})
            
            parts = message.get("parts", [])
            
            texts = []
            for part in parts:
                if isinstance(part, dict):
                    if part.get("kind") == "text":
                        texts.append(part.get("text", ""))
                    elif "text" in part:
                        texts.append(part["text"])
            
            return " ".join(texts).strip()
        except Exception as e:
            return f"Error extracting response: {e}\nRaw response: {json.dumps(response, indent=2)}"


def interactive_test():
    """
    Run an interactive test session with the Travel Agent
    """
    print("=" * 60)
    print("🌍 Travel Agent A2A Test Client")
    print("=" * 60)
    
    base_url = input("Enter server URL (default: http://localhost:8080): ").strip()
    if not base_url:
        base_url = "http://localhost:8080"
    
    client = A2ATestClient(base_url)
    
    # Fetch and display agent card (no auth required)
    print("\n📋 Fetching Agent Card...")
    try:
        agent_card = client.get_agent_card()
        print(f"✅ Connected to: {agent_card.get('name')}")
        desc = agent_card.get('description', '')[:100]
        print(f"   Description: {desc}...")
        print(f"   Version: {agent_card.get('version')}")
        skills = [s.get('name', '') for s in agent_card.get('skills', [])]
        print(f"   Skills: {', '.join(skills)}")
        
        # Check if OAuth2 is required
        security_schemes = agent_card.get('securitySchemes', {})
        if 'oauth2' in security_schemes:
            print(f"   🔐 OAuth2 authentication required")
    except Exception as e:
        print(f"❌ Failed to fetch agent card: {e}")
        return
    
    # Authenticate with OAuth2
    print("\n🔐 Authenticating...")
    if client.authenticate():
        print("✅ Authentication successful!")
    else:
        print("⚠️  Authentication failed - requests may be rejected")
    
    print("\n" + "-" * 60)
    print("Type your travel questions (or 'quit' to exit, 'new' for new conversation)")
    print("-" * 60 + "\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "quit":
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == "new":
                client.context_id = None
                client.task_id = None
                print("🔄 Started new conversation context\n")
                continue
            
            # Send message and get response
            response = client.send_message(user_input)
            
            # Extract and display the response
            agent_response = client.extract_response_text(response)
            print(f"\n🌍 Travel Agent: {agent_response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


def test_basic_flow():
    """
    Run a basic automated test of the A2A server
    """
    print("🧪 Running basic A2A flow test...")
    
    client = A2ATestClient("http://localhost:8080")
    
    # Test 1: Agent Card (no auth required)
    print("\n1️⃣ Testing Agent Card endpoint...")
    try:
        card = client.get_agent_card()
        assert "name" in card, "Agent card missing 'name'"
        assert "skills" in card, "Agent card missing 'skills'"
        print(f"   ✅ Agent Card OK - {card.get('name')}")
    except Exception as e:
        print(f"   ❌ Agent Card failed: {e}")
        return False
    
    # Test 2: OAuth2 Authentication
    print("\n2️⃣ Testing OAuth2 authentication...")
    try:
        assert client.authenticate(), "Authentication failed"
        assert client.access_token is not None, "No access token received"
        print(f"   ✅ OAuth2 Authentication OK")
        print(f"   Token preview: {client.access_token[:50]}...")
    except Exception as e:
        print(f"   ❌ OAuth2 Authentication failed: {e}")
        return False
    
    # Test 3: Send a message (requires auth)
    print("\n3️⃣ Testing message send...")
    try:
        response = client.send_message("I want to plan a trip to Paris for 5 days")
        assert "result" in response or "error" not in response, "Request failed"
        text = client.extract_response_text(response)
        assert len(text) > 0, "Empty response"
        print(f"   ✅ Message send OK")
        print(f"   Response preview: {text[:200]}...")
    except Exception as e:
        print(f"   ❌ Message send failed: {e}")
        return False
    
    # Test 4: Follow-up in same context
    print("\n4️⃣ Testing conversation context...")
    try:
        response = client.send_message("My budget is $2000")
        text = client.extract_response_text(response)
        assert len(text) > 0, "Empty response"
        print(f"   ✅ Context persistence OK")
        print(f"   Response preview: {text[:200]}...")
    except Exception as e:
        print(f"   ❌ Context test failed: {e}")
        return False
    
    # Test 5: Unauthenticated request should fail
    print("\n5️⃣ Testing unauthenticated request rejection...")
    try:
        # Create a new client without authentication
        unauth_client = A2ATestClient("http://localhost:8080")
        unauth_client.access_token = None  # Ensure no token
        
        import requests
        response = requests.post(
            "http://localhost:8080/",
            json={
                "jsonrpc": "2.0",
                "id": "test",
                "method": "message/send",
                "params": {"message": {"role": "user", "parts": [{"kind": "text", "text": "test"}], "messageId": "test-1"}}
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 401:
            print(f"   ✅ Unauthenticated request properly rejected (401)")
        else:
            print(f"   ⚠️  Expected 401, got {response.status_code}")
    except Exception as e:
        print(f"   ❌ Rejection test failed: {e}")
    
    print("\n" + "=" * 60)
    print("✅ All basic tests passed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_basic_flow()
    else:
        interactive_test()
