"""
Dynamic Agent Card with Host Detection
Automatically detects the public host from request headers
"""
import os
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from a2a.types import AgentCard
from a2a.server.apps.jsonrpc.jsonrpc_app import CallContextBuilder
from a2a.server.context import ServerCallContext
from a2a.auth.user import User

from a2a_protocol.agent_card import create_agent_card


class AnonymousUser(User):
    """Anonymous user for unauthenticated requests."""
    
    @property
    def is_authenticated(self) -> bool:
        return False
    
    @property
    def user_name(self) -> str:
        return "anonymous"


class HostAwareContextBuilder(CallContextBuilder):
    """
    Custom context builder that captures the host from request headers
    and stores it in the context state for later use.
    """
    
    def build(self, request: Request) -> ServerCallContext:
        """
        Build a ServerCallContext with host information from headers
        
        The host is determined in this order:
        1. X-Forwarded-Host header (set by load balancers/proxies)
        2. Host header
        3. A2A_PUBLIC_HOST environment variable
        4. localhost (fallback)
        """
        # Get host from headers (AWS App Runner sets X-Forwarded-Host)
        host = (
            request.headers.get("x-forwarded-host") or
            request.headers.get("host") or
            os.getenv("A2A_PUBLIC_HOST") or
            "localhost"
        )
        
        # Remove port from host if present (for agent card URL)
        if ":" in host:
            host = host.split(":")[0]
        
        # Determine if HTTPS (X-Forwarded-Proto or default for non-localhost)
        proto = request.headers.get("x-forwarded-proto", "http")
        if host != "localhost" and host != "127.0.0.1":
            proto = "https"  # Assume HTTPS for production
        
        return ServerCallContext(
            state={
                "detected_host": host,
                "detected_proto": proto,
                "request_url": str(request.url),
            },
            user=AnonymousUser(),
            requested_extensions=set(),
            activated_extensions=set(),
        )


def create_dynamic_agent_card_modifier():
    """
    Create a card modifier function that updates the URL based on detected host.
    
    Note: This modifier doesn't have access to request headers, so it uses
    environment variables as fallback. The actual host detection happens
    via the HostAwareContextBuilder for request processing.
    
    Returns:
        Callable that modifies the agent card
    """
    def modifier(card: AgentCard) -> AgentCard:
        # This is called at startup, not per-request
        # The URL in the agent card will be based on environment config
        return card
    
    return modifier


def get_base_url_from_request(request: Request) -> str:
    """
    Extract the base URL from a Starlette request.
    
    Args:
        request: The Starlette request object
        
    Returns:
        str: The base URL (e.g., "https://myapp.awsapprunner.com")
    """
    # Check X-Forwarded headers (used by proxies/load balancers)
    proto = request.headers.get("x-forwarded-proto", request.url.scheme)
    host = request.headers.get("x-forwarded-host") or request.headers.get("host")
    
    if not host:
        host = f"{request.url.hostname}"
        if request.url.port and request.url.port not in (80, 443):
            host += f":{request.url.port}"
    
    return f"{proto}://{host}"


class DynamicAgentCardMiddleware(BaseHTTPMiddleware):
    """
    Middleware that serves a dynamically-generated agent card based on
    the request's Host header.
    
    This middleware intercepts requests to /.well-known/agent-card.json
    and generates the agent card URL based on the incoming request headers.
    """
    
    def __init__(self, app, agent_card_base: AgentCard):
        super().__init__(app)
        self.agent_card_base = agent_card_base
    
    async def dispatch(self, request: Request, call_next):
        # Intercept agent card requests
        if request.url.path in ("/.well-known/agent-card.json", "/.well-known/agent.json"):
            base_url = get_base_url_from_request(request)
            
            # Create a modified agent card with the detected URL
            card_dict = self.agent_card_base.model_dump(by_alias=True, exclude_none=True)
            card_dict["url"] = base_url
            
            return JSONResponse(card_dict)
        
        return await call_next(request)
