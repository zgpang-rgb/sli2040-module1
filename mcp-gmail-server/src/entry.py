"""Cloudflare Worker entrypoint.

`workers.asgi.entrypoint` wraps the ASGI app in a WorkerEntrypoint whose fetch
handler Cloudflare invokes per request. This module is the `main` in
wrangler.jsonc and is the only file that imports the Workers runtime.
"""

from mcp_app import app
from workers.asgi import entrypoint

Default = entrypoint(app)
