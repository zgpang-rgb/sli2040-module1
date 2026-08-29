"""Configuration lookup that works both on Workers and on a normal Python host.

Cloudflare's ASGI adapter puts the Worker's bindings on the ASGI scope as
``scope["env"]`` (see workers-py ``packages/runtime-sdk/src/workers/asgi.py``),
not in ``os.environ``. Secrets set with ``wrangler secret put`` therefore have to
be read off the request, so every lookup here takes the ASGI scope.

Falling back to ``os.environ`` keeps the same code runnable under plain uvicorn
for local testing, where ``.dev.vars`` is exported into the environment instead.
"""

from __future__ import annotations

import os
from typing import Any


class MissingConfig(RuntimeError):
    """A required secret is not configured on the Worker."""


def get(scope: dict[str, Any] | None, name: str) -> str | None:
    """Return the configured value for *name*, or None when it is unset."""
    env = (scope or {}).get("env")
    if env is not None:
        # On Workers this is a JS object proxied through Pyodide, so bindings are
        # attributes rather than dict keys.
        value = getattr(env, name, None)
        if value is not None:
            return str(value)
    return os.environ.get(name)


def require(scope: dict[str, Any] | None, name: str) -> str:
    """Return the configured value for *name*, or raise if it is unset."""
    value = get(scope, name)
    if not value:
        raise MissingConfig(
            f"{name} is not set. Configure it with: pywrangler secret put {name}"
        )
    return value
