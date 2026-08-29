"""Builds the ASGI application.

Kept separate from entry.py so the exact app that runs on Workers can also be
imported and exercised under plain uvicorn, where the `workers` module does not
exist.
"""

from __future__ import annotations

from auth import BearerAuthMiddleware
from server import mcp
from starlette.middleware import Middleware

app = mcp.http_app(
    path="/mcp",
    transport="http",  # Streamable HTTP
    # Required on Workers. Cloudflare's ASGI adapter drives a full lifespan
    # startup/shutdown cycle around every single request, so nothing survives
    # between calls; a stateful session would be torn down the moment it was
    # created.
    stateless_http=True,
    middleware=[Middleware(BearerAuthMiddleware)],
)
