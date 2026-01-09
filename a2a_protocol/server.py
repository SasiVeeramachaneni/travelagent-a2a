"""
A2A Server for Travel Agent
Main server application using Starlette and A2A SDK
"""
import os
import uvicorn
from dotenv import load_dotenv

from a2a.server.apps.jsonrpc.starlette_app import A2AStarletteApplication
from a2a.server.request_handlers.default_request_handler import DefaultRequestHandler
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore

from a2a_protocol.agent_card import create_agent_card
from a2a_protocol.executor import TravelAgentExecutor

# Load environment variables
load_dotenv()


def create_a2a_app(host: str = "localhost", port: int = 8000):
    """
    Create the A2A Starlette application
    
    Args:
        host: The hostname for the agent card URL
        port: The port number
        
    Returns:
        A2AStarletteApplication: The configured A2A application
    """
    # Create the agent card
    agent_card = create_agent_card(host=host, port=port)
    
    # Create the executor
    executor = TravelAgentExecutor()
    
    # Create in-memory task store
    task_store = InMemoryTaskStore()
    
    # Create the request handler
    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=task_store
    )
    
    # Create the A2A Starlette application
    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )
    
    return app


def get_server_config():
    """
    Get server configuration from environment variables
    
    Returns:
        tuple: (host, port) configuration
    """
    host = os.getenv("A2A_HOST", "0.0.0.0")
    port = int(os.getenv("A2A_PORT", "8000"))
    return host, port


# Create the ASGI app for deployment
def create_app():
    """
    Create the ASGI application for deployment
    
    This function is called by ASGI servers like uvicorn
    """
    host, port = get_server_config()
    
    # For production, use the actual host from environment
    public_host = os.getenv("A2A_PUBLIC_HOST", host)
    
    a2a_app = create_a2a_app(host=public_host, port=port)
    return a2a_app.build()


# Application instance for ASGI servers
app = create_app()


if __name__ == "__main__":
    """
    Run the A2A server directly
    
    Usage:
        python -m a2a.server
        
    Environment variables:
        A2A_HOST: Server host (default: 0.0.0.0)
        A2A_PORT: Server port (default: 8000)
        A2A_PUBLIC_HOST: Public hostname for agent card URL
    """
    host, port = get_server_config()
    
    print(f"🚀 Starting Travel Agent A2A Server")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"📋 Agent Card: http://{host}:{port}/.well-known/agent.json")
    print("-" * 50)
    
    uvicorn.run(
        "a2a.server:app",
        host=host,
        port=port,
        reload=os.getenv("A2A_RELOAD", "false").lower() == "true"
    )
