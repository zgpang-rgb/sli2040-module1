"""Bearer-token gate in front of the MCP endpoint.

Written as raw ASGI rather than Starlette's BaseHTTPMiddleware on purpose:
BaseHTTPMiddleware buffers through an anyio task group, which interferes with
the long-lived streaming responses Streamable HTTP relies on.
"""

from __future__ import annotations

import hmac
import json
from typing import Any

import envcfg

Scope = dict[str, Any]


class BearerAuthMiddleware:
    """Reject requests whose bearer token does not match MCP_AUTH_TOKEN."""

    def __init__(self, app: Any) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        expected = envcfg.get(scope, "MCP_AUTH_TOKEN")
        if not expected:
            await _json_error(
                send,
                503,
                "server_not_configured",
                "MCP_AUTH_TOKEN is not set on this Worker; refusing all requests.",
            )
            return

        if not _token_matches(scope, expected):
            await _json_error(
                send,
                401,
                "unauthorized",
                "Missing or invalid bearer token.",
                extra_headers=[(b"www-authenticate", b'Bearer realm="mcp"')],
            )
            return

        await self.app(scope, receive, send)


def _token_matches(scope: Scope, expected: str) -> bool:
    for name, value in scope.get("headers") or []:
        if name.lower() != b"authorization":
            continue
        header = value.decode("latin-1").strip()
        scheme, _, token = header.partition(" ")
        if scheme.lower() != "bearer":
            return False
        # Constant-time compare so a wrong token leaks nothing through timing.
        return hmac.compare_digest(token.strip(), expected)
    return False


async def _json_error(
    send: Any,
    status: int,
    code: str,
    message: str,
    extra_headers: list[tuple[bytes, bytes]] | None = None,
) -> None:
    body = json.dumps({"error": code, "message": message}).encode()
    headers = [
        (b"content-type", b"application/json"),
        (b"content-length", str(len(body)).encode()),
    ]
    headers.extend(extra_headers or [])
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": body})
