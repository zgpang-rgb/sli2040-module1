"""Minimal JSON-over-HTTPS helper.

On Cloudflare Workers the supported way to make an outbound request is the
runtime's own ``fetch``, reached through the Pyodide FFI. ``httpx`` imports fine
under Pyodide but its transport layer is not part of the Workers-supported
surface, so it is used only as the local-development fallback.

Both paths are kept behind ``request_json`` so the rest of the server never has
to care which runtime it is on.
"""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlencode

try:  # pragma: no cover - only importable inside the Workers runtime
    from js import Object as _JsObject
    from js import fetch as _js_fetch
    from pyodide.ffi import to_js as _to_js

    ON_WORKERS = True
except ImportError:  # pragma: no cover - local development
    _JsObject = None
    _js_fetch = None
    _to_js = None
    ON_WORKERS = False


class HTTPError(RuntimeError):
    """A non-2xx response from an upstream API."""

    def __init__(self, status: int, url: str, body: str) -> None:
        self.status = status
        self.url = url
        self.body = body
        super().__init__(f"HTTP {status} from {url}: {body[:400]}")


async def request_json(
    method: str,
    url: str,
    *,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    form: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Perform an HTTP request and decode the JSON response body."""
    if params:
        url = f"{url}?{urlencode(params)}"

    request_headers = dict(headers or {})
    body: str | None = None
    if form is not None:
        body = urlencode(form)
        request_headers["Content-Type"] = "application/x-www-form-urlencoded"

    if ON_WORKERS:
        status, text = await _fetch_via_workers(method, url, request_headers, body)
    else:
        status, text = await _fetch_via_httpx(method, url, request_headers, body)

    if status < 200 or status >= 300:
        raise HTTPError(status, url, text)
    return json.loads(text)


async def _fetch_via_workers(
    method: str, url: str, headers: dict[str, str], body: str | None
) -> tuple[int, str]:
    options: dict[str, Any] = {"method": method, "headers": headers}
    if body is not None:
        options["body"] = body
    # dict_converter=Object.fromEntries turns the (nested) Python dicts into real
    # JS objects; without it Pyodide produces a Map, which fetch() rejects.
    js_options = _to_js(options, dict_converter=_JsObject.fromEntries)
    response = await _js_fetch(url, js_options)
    text = await response.text()
    return int(response.status), str(text)


async def _fetch_via_httpx(
    method: str, url: str, headers: dict[str, str], body: str | None
) -> tuple[int, str]:
    import httpx

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request(method, url, headers=headers, content=body)
        return response.status_code, response.text
