# Azure OpenAI Integration Guide

This document explains how the Travel Agent integrates with Azure OpenAI using Azure AD client credentials.

## Architecture Overview

```
Travel Agent Application
    ↓
AI Service (services/ai_service.py)
    ↓
Azure OpenAI Client (services/azure_openai_client.py)
    ↓
Azure AD Authentication → Azure OpenAI API
```

## Authentication Flow

1. **Client Credentials Grant**
   - Application uses Client ID and Client Secret
   - Requests access token from Azure AD
   - Token is cached and refreshed automatically

2. **API Calls**
   - Access token included in Authorization header
   - Calls made to Azure OpenAI endpoint
   - Responses parsed and returned to application

## File Structure

### Core AI Files

- **`services/azure_openai_client.py`**
  - Handles Azure AD authentication
  - Manages token lifecycle
  - Makes API calls to Azure OpenAI
  - Provides chat completion interface

- **`services/ai_service.py`**
  - High-level AI service wrapper
  - Manages conversation history
  - Provides domain-specific AI methods
  - Falls back to basic mode if AI unavailable

### Integration Points

- **`agent/travel_agent.py`**
  - Main agent uses AIService
  - Switches between AI and rule-based modes
  - Provides AI-enhanced responses

- **`main.py`**
  - Loads environment variables
  - Tests AI connection on startup
  - Shows AI status to user

## Configuration

### Environment Variables (.env)

```bash
# Required for Azure OpenAI
OPENAI_ENDPOINT=https://your-resource.openai.azure.com
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret

# Azure AD Configuration
TOKEN_URL=https://login.microsoftonline.com/common/oauth2/v2.0/token
TOKEN_SCOPE=https://cognitiveservices.azure.com/.default

# Deployment Settings
OPENAI_DEPLOYMENT=gpt-4
OPENAI_API_VERSION=2024-02-15-preview

# Optional: Model Parameters
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000
```

### Config Class (config.py)

The `Config` class loads these environment variables and provides them to the application:

```python
from config import Config

# Access configuration
endpoint = Config.OPENAI_ENDPOINT
deployment = Config.OPENAI_DEPLOYMENT
```

## Usage Examples

### Basic Usage in Code

```python
from services.ai_service import AIService

# Initialize AI service
ai_service = AIService()

# Check if AI is enabled
if ai_service.enabled:
    # Get AI response
    response = ai_service.get_ai_response(
        "I want to visit Paris",
        context={'budget': 3000, 'duration': 5}
    )
    print(response)
```

### Using the OpenAI Client Directly

```python
from services.azure_openai_client import get_openai_client

# Get client instance
client = get_openai_client()

# Create messages
messages = [
    client.create_system_message("You are a travel expert."),
    client.create_user_message("Tell me about Paris.")
]

# Get completion
response = client.chat_completion(messages)
content = client.get_response_content(response)
print(content)
```

## Testing

### Quick Credential Test

```bash
python test_credentials.py
```

This tests:
1. ✅ Credentials loaded from .env
2. ✅ Azure AD authentication working
3. ✅ Azure OpenAI API responding

### Full Setup Check

```bash
python setup_check.py
```

This verifies:
1. ✅ Python version
2. ✅ Dependencies installed
3. ✅ Environment configured
4. ✅ Azure connection working

### Test from Application

```bash
python main.py
# Type: test
```

## Fallback Behavior

The application gracefully handles missing credentials:

1. **AI Enabled**: Uses Azure OpenAI for natural conversations
2. **AI Disabled**: Falls back to rule-based responses
3. **Partial Config**: Shows warning but continues in basic mode

```python
# In ai_service.py
if not self.enabled:
    return self._get_fallback_response(user_message)
```

## Token Management

The client automatically handles token lifecycle:

```python
def _get_access_token(self) -> str:
    # Check if token is still valid
    if self._access_token and self._token_expiry:
        if datetime.now() < self._token_expiry - timedelta(minutes=5):
            return self._access_token
    
    # Request new token if expired
    # ...
```

Tokens are:
- ✅ Cached for reuse
- ✅ Automatically refreshed before expiry
- ✅ Thread-safe (singleton pattern)

## Error Handling

The system handles various error scenarios:

### Missing Credentials
```python
raise ValueError(
    f"Missing required Azure OpenAI configuration: {', '.join(missing)}"
)
```

### Authentication Failures
```python
except requests.exceptions.RequestException as e:
    raise Exception(f"Failed to obtain Azure AD access token: {e}")
```

### API Call Failures
```python
except requests.exceptions.RequestException as e:
    raise Exception(f"Azure OpenAI API request failed: {e}")
```

## Security Best Practices

1. **Never commit .env file**
   - Added to .gitignore
   - Use .env.example for template

2. **Secure credential storage**
   - Use environment variables
   - Consider Azure Key Vault for production

3. **Token security**
   - Tokens cached in memory only
   - Automatically expired and refreshed

4. **API key rotation**
   - Update CLIENT_SECRET in .env
   - Restart application

## Troubleshooting

### "Missing required Azure OpenAI configuration"
- Check .env file exists
- Verify all required variables are set
- Ensure no placeholder values remain

### "Failed to obtain Azure AD access token"
- Verify TENANT_ID, CLIENT_ID, CLIENT_SECRET
- Check App Registration permissions
- Ensure TOKEN_URL and TOKEN_SCOPE are correct

### "Azure OpenAI API request failed"
- Verify OPENAI_ENDPOINT is correct
- Check deployment name matches Azure
- Ensure App Registration has Cognitive Services role

### Connection test fails
- Run `python test_credentials.py` for detailed diagnostics
- Check Azure portal for service status
- Verify network connectivity

## Advanced Configuration

### Using Specific Tenant

Replace 'common' with your tenant ID in TOKEN_URL:
```bash
TOKEN_URL=https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/token
```

### Custom Deployment

Change deployment name and model:
```bash
OPENAI_DEPLOYMENT=gpt-4-32k
OPENAI_TEMPERATURE=0.8
OPENAI_MAX_TOKENS=4000
```

### Multiple Environments

Create separate .env files:
- `.env.development`
- `.env.production`
- `.env.testing`

Load specific environment:
```bash
export ENV_FILE=.env.production
python main.py
```

## API Reference

### AzureOpenAIClient Methods

- `chat_completion(messages, temperature, max_tokens, stream)` - Create chat completion
- `get_response_content(api_response)` - Extract content from response
- `create_system_message(content)` - Create system message
- `create_user_message(content)` - Create user message
- `create_assistant_message(content)` - Create assistant message
- `test_connection()` - Test API connection

### AIService Methods

- `get_ai_response(user_message, context)` - Get AI response with context
- `enhance_itinerary(itinerary)` - Enhance itinerary with AI insights
- `get_destination_insights(destination, interests)` - Get destination insights
- `reset_conversation()` - Reset conversation history
- `test_connection()` - Test connection

## Performance Considerations

- **Token Caching**: Reduces auth overhead
- **Conversation History**: Limited to 20 messages to control costs
- **Timeout Handling**: 10-second timeout on API calls
- **Graceful Degradation**: Falls back to basic mode on failure

## Cost Management

Azure OpenAI charges based on:
- Tokens used (input + output)
- Model type (GPT-4 vs GPT-3.5)
- API calls made

To manage costs:
1. Use appropriate max_tokens settings
2. Limit conversation history size
3. Monitor usage in Azure portal
4. Consider GPT-3.5 for non-critical tasks

## Support

For issues or questions:
1. Check this guide
2. Run diagnostic scripts
3. Review Azure portal logs
4. Check application logs

## Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/cognitive-services/openai/)
- [Azure AD App Registrations](https://learn.microsoft.com/azure/active-directory/develop/quickstart-register-app)
- [Python requests Library](https://requests.readthedocs.io/)
