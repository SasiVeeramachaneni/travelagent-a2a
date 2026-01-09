"""
Travel Agent A2A Application Entry Point
This is the main entry point for AWS App Runner deployment

AWS App Runner will look for an 'app' variable in this file

The agent card URL is automatically detected from request headers,
so you don't need to set A2A_PUBLIC_HOST manually.

OAuth2 Authentication:
- Token URL: /oauth/token
- Grant Type: client_credentials
- Set OAUTH2_CLIENT_ID and OAUTH2_CLIENT_SECRET environment variables
"""
import os
import sys

# Ensure the project root is in the path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from a2a.server.apps.jsonrpc.starlette_app import A2AStarletteApplication
from a2a.server.request_handlers.default_request_handler import DefaultRequestHandler
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore

from a2a_protocol.agent_card import create_agent_card
from a2a_protocol.executor import TravelAgentExecutor
from a2a_protocol.dynamic_host import (
    HostAwareContextBuilder,
    DynamicAgentCardMiddleware,
)
from a2a_protocol.oauth2 import (
    OAuth2Middleware,
    print_oauth2_credentials,
    DEFAULT_CLIENT_ID,
    DEFAULT_CLIENT_SECRET,
    OAUTH2_SCOPE,
)


def create_application(require_oauth2: bool = True):
    """
    Create the ASGI application for AWS App Runner
    
    AWS App Runner provides:
    - PORT environment variable (usually 8080)
    - The application should listen on 0.0.0.0
    
    The agent card URL is automatically detected from request headers:
    - X-Forwarded-Host (set by AWS App Runner / load balancers)
    - Host header (fallback)
    
    Args:
        require_oauth2: Whether to require OAuth2 authentication (default: True)
    
    Returns:
        Starlette application instance
    """
    # Get configuration from environment
    port = int(os.getenv("PORT", "8080"))
    
    # Check if OAuth2 is disabled via environment
    oauth2_enabled = os.getenv("OAUTH2_ENABLED", "true").lower() == "true"
    require_auth = require_oauth2 and oauth2_enabled
    
    # Create agent card with placeholder URL
    # The actual URL will be determined dynamically from request headers
    agent_card = create_agent_card(
        host="localhost",  # Placeholder - will be overridden by middleware
        port=port,
        version=os.getenv("APP_VERSION", "1.0.0"),
        include_oauth2=oauth2_enabled
    )
    
    # Create executor (wraps our Travel Agent)
    executor = TravelAgentExecutor()
    
    # Create in-memory task store
    task_store = InMemoryTaskStore()
    
    # Create request handler
    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=task_store
    )
    
    # Create A2A application with custom context builder
    a2a_app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
        context_builder=HostAwareContextBuilder(),
    )
    
    # Build the Starlette app
    starlette_app = a2a_app.build()
    
    # Add middleware for dynamic agent card URL
    starlette_app = DynamicAgentCardMiddleware(starlette_app, agent_card)
    
    # Add OAuth2 middleware (must be outermost to intercept all requests)
    starlette_app = OAuth2Middleware(starlette_app, require_auth=require_auth)
    
    return starlette_app


# Create the application instance
# AWS App Runner looks for 'app' or 'application' variable
app = create_application()


if __name__ == "__main__":
    """
    Run the application locally for testing
    """
    import uvicorn
    
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")
    oauth2_enabled = os.getenv("OAUTH2_ENABLED", "true").lower() == "true"
    
    print("=" * 60)
    print("🌍 Travel Agent A2A Server")
    print("=" * 60)
    print(f"📍 Running on: http://{host}:{port}")
    print(f"📋 Agent Card: http://localhost:{port}/.well-known/agent-card.json")
    print(f"🤖 A2A Endpoint: http://localhost:{port}/")
    print(f"🔐 OAuth2: {'Enabled' if oauth2_enabled else 'Disabled'}")
    
    if oauth2_enabled:
        print(f"🔑 Token URL: http://localhost:{port}/oauth/token")
        print_oauth2_credentials()
    
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
