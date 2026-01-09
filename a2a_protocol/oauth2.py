"""
OAuth2 Client Credentials Authentication for A2A Travel Agent

This module provides OAuth2 authentication using the Client Credentials flow,
which is ideal for machine-to-machine (agent-to-agent) communication.

Token URL: /oauth/token
Grant Type: client_credentials
"""
import os
import secrets
import hashlib
import time
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

import jwt
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Route


# =============================================================================
# Configuration
# =============================================================================

# JWT Settings
JWT_SECRET_KEY = os.getenv("OAUTH2_JWT_SECRET", secrets.token_urlsafe(32))
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRY_SECONDS = int(os.getenv("OAUTH2_TOKEN_EXPIRY", "3600"))  # 1 hour default

# OAuth2 Scope
OAUTH2_SCOPE = "a2a:travel-agent"

# Default client credentials (can be overridden by environment variables)
# In production, ALWAYS set these via environment variables
DEFAULT_CLIENT_ID = os.getenv("OAUTH2_CLIENT_ID", "")
# Use a stable default secret for development - MUST be overridden in production
DEFAULT_CLIENT_SECRET = os.getenv("OAUTH2_CLIENT_SECRET", "")


# =============================================================================
# Client Registry
# =============================================================================

@dataclass
class OAuth2Client:
    """Represents a registered OAuth2 client."""
    client_id: str
    client_secret_hash: str
    name: str
    scopes: list = field(default_factory=lambda: [OAUTH2_SCOPE])
    enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ClientRegistry:
    """
    Registry of OAuth2 clients.
    
    In production, this should be backed by a database.
    For this implementation, we use in-memory storage with environment config.
    """
    
    def __init__(self):
        self._clients: Dict[str, OAuth2Client] = {}
        self._initialize_default_client()
    
    def _hash_secret(self, secret: str) -> str:
        """Hash a client secret using SHA256."""
        return hashlib.sha256(secret.encode()).hexdigest()
    
    def _initialize_default_client(self):
        """Initialize the default client from environment variables."""
        self.register_client(
            client_id=DEFAULT_CLIENT_ID,
            client_secret=DEFAULT_CLIENT_SECRET,
            name="Default Travel Agent Client"
        )
    
    def register_client(
        self,
        client_id: str,
        client_secret: str,
        name: str,
        scopes: list = None
    ) -> OAuth2Client:
        """Register a new OAuth2 client."""
        client = OAuth2Client(
            client_id=client_id,
            client_secret_hash=self._hash_secret(client_secret),
            name=name,
            scopes=scopes or [OAUTH2_SCOPE]
        )
        self._clients[client_id] = client
        return client
    
    def validate_client(self, client_id: str, client_secret: str) -> Optional[OAuth2Client]:
        """
        Validate client credentials.
        
        Returns the client if valid, None otherwise.
        """
        client = self._clients.get(client_id)
        if not client:
            return None
        
        if not client.enabled:
            return None
        
        if client.client_secret_hash != self._hash_secret(client_secret):
            return None
        
        return client
    
    def get_client(self, client_id: str) -> Optional[OAuth2Client]:
        """Get a client by ID."""
        return self._clients.get(client_id)


# Global client registry
client_registry = ClientRegistry()


# =============================================================================
# Token Management
# =============================================================================

@dataclass
class TokenPayload:
    """JWT token payload."""
    client_id: str
    scopes: list
    exp: int  # Expiration timestamp
    iat: int  # Issued at timestamp
    jti: str  # JWT ID (unique identifier)


def generate_access_token(client: OAuth2Client, requested_scopes: list = None) -> Dict[str, Any]:
    """
    Generate an OAuth2 access token for a client.
    
    Args:
        client: The authenticated OAuth2 client
        requested_scopes: Scopes requested by the client (must be subset of allowed scopes)
    
    Returns:
        Dict with access_token, token_type, expires_in, and scope
    """
    now = int(time.time())
    expiry = now + TOKEN_EXPIRY_SECONDS
    
    # Validate requested scopes
    if requested_scopes:
        granted_scopes = [s for s in requested_scopes if s in client.scopes]
    else:
        granted_scopes = client.scopes
    
    # Create JWT payload
    payload = {
        "client_id": client.client_id,
        "scopes": granted_scopes,
        "exp": expiry,
        "iat": now,
        "jti": secrets.token_urlsafe(16),
        "iss": "travel-agent-oauth2",
        "aud": "travel-agent-a2a"
    }
    
    # Generate JWT
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    return {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": TOKEN_EXPIRY_SECONDS,
        "scope": " ".join(granted_scopes)
    }


def validate_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Validate an access token and return its payload.
    
    Args:
        token: The JWT access token
    
    Returns:
        Token payload dict if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            audience="travel-agent-a2a"
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# =============================================================================
# OAuth2 Token Endpoint
# =============================================================================

async def token_endpoint(request: Request) -> JSONResponse:
    """
    OAuth2 Token Endpoint.
    
    POST /oauth/token
    
    Supports:
    - grant_type=client_credentials
    - Client credentials in request body or Basic Auth header
    
    Request body (application/x-www-form-urlencoded or application/json):
        grant_type: "client_credentials" (required)
        client_id: string (required if not using Basic Auth)
        client_secret: string (required if not using Basic Auth)
        scope: space-separated scopes (optional)
    
    Response:
        {
            "access_token": "eyJ...",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "a2a:travel-agent"
        }
    """
    # Parse request
    content_type = request.headers.get("content-type", "")
    
    if "application/json" in content_type:
        try:
            body = await request.json()
        except:
            return JSONResponse(
                {"error": "invalid_request", "error_description": "Invalid JSON body"},
                status_code=400
            )
    else:
        # application/x-www-form-urlencoded
        form = await request.form()
        body = dict(form)
    
    # Extract credentials
    client_id = body.get("client_id")
    client_secret = body.get("client_secret")
    
    # Check for Basic Auth header if credentials not in body
    if not client_id or not client_secret:
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Basic "):
            import base64
            try:
                decoded = base64.b64decode(auth_header[6:]).decode("utf-8")
                client_id, client_secret = decoded.split(":", 1)
            except:
                pass
    
    # Validate grant_type
    grant_type = body.get("grant_type")
    if grant_type != "client_credentials":
        return JSONResponse(
            {
                "error": "unsupported_grant_type",
                "error_description": "Only 'client_credentials' grant type is supported"
            },
            status_code=400
        )
    
    # Validate client credentials
    if not client_id or not client_secret:
        return JSONResponse(
            {
                "error": "invalid_request",
                "error_description": "client_id and client_secret are required"
            },
            status_code=400
        )
    
    client = client_registry.validate_client(client_id, client_secret)
    if not client:
        return JSONResponse(
            {
                "error": "invalid_client",
                "error_description": "Invalid client credentials"
            },
            status_code=401
        )
    
    # Parse requested scopes
    scope_str = body.get("scope", "")
    requested_scopes = scope_str.split() if scope_str else None
    
    # Generate token
    token_response = generate_access_token(client, requested_scopes)
    
    return JSONResponse(token_response)


# =============================================================================
# OAuth2 Authentication Middleware
# =============================================================================

class OAuth2Middleware(BaseHTTPMiddleware):
    """
    Middleware to enforce OAuth2 authentication on protected endpoints.
    
    Protected endpoints require a valid Bearer token in the Authorization header.
    The agent card endpoint (/.well-known/agent-card.json) and token endpoint
    are not protected to allow discovery and authentication.
    
    Root path "/" is protected for POST requests (A2A messaging) but allowed
    for GET requests (discovery/redirect).
    """
    
    # Endpoints that don't require authentication
    PUBLIC_PATHS = {
        "/.well-known/agent-card.json",
        "/.well-known/agent.json",  # Legacy path
        "/oauth/token",
        "/health",
    }
    
    def __init__(self, app, require_auth: bool = True):
        super().__init__(app)
        self.require_auth = require_auth
    
    async def dispatch(self, request: Request, call_next):
        # Handle token endpoint first (it's handled by this middleware)
        if request.url.path == "/oauth/token":
            return await token_endpoint(request)
        
        # Skip auth for public paths (GET or POST)
        if request.url.path in self.PUBLIC_PATHS:
            return await call_next(request)
        
        # Skip auth for GET requests to root (agent card redirect/discovery)
        if request.method == "GET" and request.url.path == "/":
            return await call_next(request)
        
        # Require authentication for other endpoints
        if self.require_auth:
            auth_header = request.headers.get("authorization", "")
            
            if not auth_header.startswith("Bearer "):
                return JSONResponse(
                    {
                        "error": "unauthorized",
                        "error_description": "Bearer token required"
                    },
                    status_code=401,
                    headers={"WWW-Authenticate": "Bearer"}
                )
            
            token = auth_header[7:]  # Remove "Bearer " prefix
            payload = validate_access_token(token)
            
            if not payload:
                return JSONResponse(
                    {
                        "error": "invalid_token",
                        "error_description": "Invalid or expired access token"
                    },
                    status_code=401,
                    headers={"WWW-Authenticate": "Bearer error=\"invalid_token\""}
                )
            
            # Add token payload to request state for downstream use
            request.state.oauth2_client_id = payload.get("client_id")
            request.state.oauth2_scopes = payload.get("scopes", [])
        
        return await call_next(request)


# =============================================================================
# Helper Functions
# =============================================================================

def get_oauth2_config() -> Dict[str, Any]:
    """
    Get OAuth2 configuration for display/documentation.
    
    Returns config without exposing secrets.
    """
    return {
        "token_url": "/oauth/token",
        "grant_type": "client_credentials",
        "scope": OAUTH2_SCOPE,
        "token_expiry_seconds": TOKEN_EXPIRY_SECONDS,
        "client_id": DEFAULT_CLIENT_ID,
        # Note: client_secret should be retrieved securely, not exposed
    }


def print_oauth2_credentials():
    """Print OAuth2 credentials for setup (use only in development)."""
    print("\n" + "=" * 60)
    print("🔐 OAuth2 Credentials (Client Credentials Flow)")
    print("=" * 60)
    print(f"Token URL:     /oauth/token")
    print(f"Grant Type:    client_credentials")
    print(f"Client ID:     {DEFAULT_CLIENT_ID}")
    print(f"Client Secret: {DEFAULT_CLIENT_SECRET}")
    print(f"Scope:         {OAUTH2_SCOPE}")
    print(f"Token Expiry:  {TOKEN_EXPIRY_SECONDS} seconds")
    print("=" * 60 + "\n")
