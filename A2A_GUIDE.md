# A2A Protocol Implementation Guide

This document describes the A2A (Agent-to-Agent) protocol implementation for the Travel Agent, enabling other AI agents to interact with it programmatically.

## Overview

The A2A protocol allows agents to discover and communicate with each other using a standardized JSON-RPC 2.0 over HTTP(S) interface. Our Travel Agent exposes its capabilities through an Agent Card and accepts requests via the A2A protocol.

**Security:** The agent requires OAuth2 authentication using the Client Credentials flow. See the [OAuth2 Authentication](#oauth2-authentication) section below.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Other AI Agents                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ A2A Protocol (JSON-RPC 2.0)
                              │ + OAuth2 Bearer Token
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     A2A Server (app.py)                     │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              OAuth2 Middleware                        │  │
│  │  - Token validation                                  │  │
│  │  - /oauth/token endpoint                             │  │
│  └───────────────────────────────────────────────────────┘  │
│                              │                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         A2AStarletteApplication                       │  │
│  │  - /.well-known/agent-card.json (Agent Card)         │  │
│  │  - / (A2A Endpoint - requires auth)                  │  │
│  └───────────────────────────────────────────────────────┘  │
│                              │                               │
│                              ▼                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         TravelAgentExecutor (a2a/executor.py)        │  │
│  │  - Receives A2A Messages                              │  │
│  │  - Extracts text from Parts                          │  │
│  │  - Maintains conversation context                     │  │
│  └───────────────────────────────────────────────────────┘  │
│                              │                               │
│                              ▼                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              TravelAgent (agent/travel_agent.py)     │  │
│  │  - AI-powered travel planning                         │  │
│  │  - Budget calculation                                 │  │
│  │  - Itinerary creation                                │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## OAuth2 Authentication

The Travel Agent A2A endpoint requires OAuth2 authentication using the **Client Credentials** flow. This is standard for machine-to-machine (M2M) communication between agents.

### Credentials (Development)

| Parameter | Value |
|-----------|-------|
| **Token URL** | `/oauth/token` |
| **Grant Type** | `client_credentials` |
| **Client ID** | `travel-agent-client` |
| **Client Secret** | `dev-secret-change-in-production-12345` |
| **Scope** | `a2a:travel-agent` |
| **Token Expiry** | 3600 seconds (1 hour) |

> ⚠️ **Production Security**: Always set `OAUTH2_CLIENT_ID`, `OAUTH2_CLIENT_SECRET`, and `OAUTH2_JWT_SECRET` environment variables with secure values in production!

### Step 1: Obtain Access Token

```bash
curl -X POST http://localhost:8080/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=travel-agent-client&client_secret=dev-secret-change-in-production-12345&scope=a2a:travel-agent"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "a2a:travel-agent"
}
```

### Step 2: Use Token in A2A Requests

Include the access token in the `Authorization` header:

```bash
curl -X POST http://localhost:8080/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "Plan a trip to Paris"}],
        "messageId": "msg-123"
      }
    }
  }'
```

### Public Endpoints (No Auth Required)

These endpoints are publicly accessible for discovery:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/.well-known/agent-card.json` | GET | Agent discovery document |
| `/oauth/token` | POST | OAuth2 token endpoint |
| `/health` | GET | Health check |

### Environment Variables

Configure OAuth2 in production:

```bash
# Required - use strong, unique values
OAUTH2_CLIENT_ID=your-client-id
OAUTH2_CLIENT_SECRET=your-secure-secret-minimum-32-chars
OAUTH2_JWT_SECRET=your-jwt-signing-secret-minimum-32-chars

# Optional
OAUTH2_TOKEN_EXPIRY=3600  # Token expiry in seconds
OAUTH2_ENABLED=true       # Set to false to disable auth
```

## Files Structure

```
a2a_protocol/
├── __init__.py          # Package exports
├── agent_card.py        # Agent Card definition (discovery)
├── executor.py          # TravelAgentExecutor (request handler)
├── oauth2.py            # OAuth2 authentication (NEW)
├── dynamic_host.py      # Dynamic host detection middleware
└── server.py            # Alternative server entry point

app.py                   # Main ASGI app for AWS App Runner
apprunner.yaml           # AWS App Runner configuration
Procfile                 # Alternative deployment (Heroku-style)
test_a2a_client.py       # Test client for A2A server
```

## Agent Card

The Agent Card is a discovery document that describes the agent's capabilities. It's served at `/.well-known/agent-card.json`.

The agent card now includes OAuth2 security scheme information:

```json
{
  "securitySchemes": {
    "oauth2": {
      "type": "oauth2",
      "description": "OAuth2 Client Credentials authentication",
      "flows": {
        "clientCredentials": {
          "tokenUrl": "/oauth/token",
          "scopes": {
            "a2a:travel-agent": "Access to Travel Agent A2A endpoints"
          }
        }
      }
    }
  },
  "security": [
    {"oauth2": ["a2a:travel-agent"]}
  ]
}
```

### Skills Exposed

| Skill ID | Name | Description |
|----------|------|-------------|
| `plan_trip` | Plan Trip | Complete trip planning with recommendations |
| `get_recommendations` | Get Travel Recommendations | Personalized destination/activity recommendations |
| `calculate_budget` | Calculate Trip Budget | Comprehensive budget estimation |
| `create_itinerary` | Create Detailed Itinerary | Day-by-day travel schedules |
| `travel_info` | Travel Information | Visa, weather, culture, safety info |
| `booking_assistance` | Booking Assistance | Help with booking flights/hotels |

### Example Agent Card Response

```json
{
  "name": "Travel Agent",
  "description": "An intelligent AI-powered travel agent...",
  "url": "https://your-app.aws-apprunner.com",
  "version": "1.0.0",
  "capabilities": {
    "streaming": false,
    "push_notifications": false,
    "state_transition_history": false
  },
  "skills": [
    {
      "id": "plan_trip",
      "name": "Plan Trip",
      "description": "Plan a complete trip...",
      "tags": ["travel", "planning", "trip", "vacation"],
      "examples": [
        "Plan a 7-day trip to Tokyo with a budget of $3000"
      ]
    }
  ],
  "default_input_modes": ["text/plain"],
  "default_output_modes": ["text/plain"]
}
```

## A2A Protocol Usage

### Sending a Message

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "id": "unique-request-id",
  "params": {
    "message": {
      "role": "user",
      "message_id": "msg-123",
      "parts": [
        {
          "kind": "text",
          "text": "Plan a 5-day trip to Paris with a budget of $2000"
        }
      ],
      "context_id": "conv-456",
      "task_id": "task-789"
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": "unique-request-id",
  "result": {
    "task_id": "task-789",
    "context_id": "conv-456",
    "status": {
      "state": "completed",
      "message": {
        "role": "agent",
        "parts": [
          {
            "kind": "text",
            "text": "I'd be happy to help you plan a 5-day trip to Paris..."
          }
        ]
      }
    }
  }
}
```

### Maintaining Conversation Context

Use the same `context_id` across multiple messages to maintain conversation state:

```json
// First message
{"params": {"message": {"context_id": "conv-456", "text": "Plan trip to Paris"}}}

// Follow-up (same context_id)
{"params": {"message": {"context_id": "conv-456", "text": "My budget is $2000"}}}
```

## Running Locally

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
# Copy and configure .env
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

### 3. Start the Server

```bash
# Option 1: Using app.py directly
python app.py

# Option 2: Using uvicorn
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

### 4. Test the Server

```bash
# Run interactive test client
python test_a2a_client.py

# Or run automated tests
python test_a2a_client.py --test

# Fetch agent card manually
curl http://localhost:8080/.well-known/agent.json
```

## Deploying to AWS App Runner

### Prerequisites

- AWS Account with App Runner access
- Source code in GitHub or AWS CodeCommit
- Environment variables configured in App Runner

### Deployment Steps

1. **Create App Runner Service**
   - Go to AWS App Runner Console
   - Click "Create service"
   - Choose "Source code repository"
   - Connect your GitHub/CodeCommit repository

2. **Configure Build Settings**
   - Runtime: Python 3.12
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - Or use the `apprunner.yaml` file for automatic configuration

3. **Configure Environment Variables**
   - Add all variables from `.env.example`
   - Set `A2A_PUBLIC_HOST` to your App Runner service URL

4. **Deploy**
   - App Runner will automatically build and deploy
   - Service URL will be provided (e.g., `https://xxxxx.us-east-1.awsapprunner.com`)

### Environment Variables for App Runner

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_ENDPOINT` | Azure OpenAI endpoint | Yes |
| `TENANT_ID` | Azure AD tenant ID | Yes |
| `CLIENT_ID` | Azure AD client ID | Yes |
| `CLIENT_SECRET` | Azure AD client secret | Yes |
| `OPENAI_DEPLOYMENT` | Model deployment name | Yes |
| `A2A_PUBLIC_HOST` | Public URL for agent card | Auto-set |

## Integration Example

Here's how another agent can integrate with the Travel Agent:

```python
import requests

class TravelAgentClient:
    def __init__(self, url):
        self.url = url
    
    def plan_trip(self, destination, duration, budget):
        message = f"Plan a {duration}-day trip to {destination} with a budget of ${budget}"
        
        response = requests.post(self.url, json={
            "jsonrpc": "2.0",
            "method": "message/send",
            "id": "1",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"kind": "text", "text": message}],
                    "context_id": "my-context",
                    "task_id": "task-1"
                }
            }
        })
        
        return response.json()

# Usage
client = TravelAgentClient("https://your-travel-agent.awsapprunner.com")
result = client.plan_trip("Tokyo", 7, 3000)
```

## Troubleshooting

### Common Issues

1. **Agent Card Not Found**
   - Ensure server is running
   - Check URL: `/.well-known/agent.json`

2. **Empty Responses**
   - Verify Azure OpenAI credentials
   - Check `OPENAI_DEPLOYMENT` is correct

3. **Connection Refused**
   - Server not running or wrong port
   - Check firewall settings

4. **AWS App Runner Issues**
   - Check CloudWatch logs
   - Verify environment variables are set
   - Ensure PORT is not hardcoded (use `$PORT`)

## Security Considerations

- Use HTTPS in production
- Secure Azure credentials using AWS Secrets Manager
- Consider adding authentication for sensitive operations
- Rate limiting recommended for production use
