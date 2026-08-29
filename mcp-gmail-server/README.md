# gmail-mcp — a remote MCP server for Claude

One tool, `get_latest_email_from_sender`, served over **Streamable HTTP** from a
**Cloudflare Python Worker**, built with **FastMCP**.

```
Claude ──HTTPS──> Worker (Pyodide) ──> FastMCP ──> Gmail REST API
                     bearer check      one tool     read-only
```

## Layout

| File | Role |
| --- | --- |
| `src/entry.py` | Worker entrypoint; the only file importing the Workers runtime |
| `src/mcp_app.py` | Builds the ASGI app (kept separate so it runs under uvicorn too) |
| `src/server.py` | The `FastMCP` instance and the tool |
| `src/gmail.py` | Gmail REST calls + MIME body extraction |
| `src/auth.py` | Bearer-token ASGI middleware |
| `src/http_client.py` | Workers `fetch` on Workers, `httpx` locally |
| `src/envcfg.py` | Reads secrets from the ASGI scope, not `os.environ` |

## 1. Get a Gmail refresh token

1. In [Google Cloud Console](https://console.cloud.google.com/), create a
   project and **enable the Gmail API**.
2. Configure the OAuth consent screen. While it is in *Testing*, add your own
   address under **Test users**.
3. Create an **OAuth client ID** of type **Desktop app**. Note the client ID and
   client secret.
4. Get a refresh token for scope
   `https://www.googleapis.com/auth/gmail.readonly`. The quickest route is
   [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/):
   gear icon → *Use your own OAuth credentials* → paste your ID and secret →
   authorize that scope → **Exchange authorization code for tokens**.

> Read-only scope is deliberate. This server can never send, delete or modify
> mail, so a leaked token cannot be used to act as you.

## 2. Set the secrets

```bash
cd mcp-gmail-server

# Generate the token Claude will present:
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

uvx --from workers-py pywrangler secret put GOOGLE_CLIENT_ID
uvx --from workers-py pywrangler secret put GOOGLE_CLIENT_SECRET
uvx --from workers-py pywrangler secret put GMAIL_REFRESH_TOKEN
uvx --from workers-py pywrangler secret put MCP_AUTH_TOKEN
```

For local runs, copy `.dev.vars.example` to `.dev.vars` and fill it in.
`.dev.vars` is gitignored — never commit it.

If `MCP_AUTH_TOKEN` is unset the server answers **503 to everything**. It fails
closed rather than serving your mailbox unauthenticated.

## 3. Deploy

```bash
uvx --from workers-py pywrangler deploy
```

`pywrangler deploy` runs `sync` first, which resolves dependencies against the
Pyodide index and vendors them into `python_modules/`. **Plain
`npx wrangler deploy` will not work** — it skips the Python vendoring step.

Requires `uv >= 0.12.3` and Node (for the wrangler it shells out to).

## 4. Add to Claude

```
https://<worker-name>.<your-subdomain>.workers.dev/mcp
```

With the default `name` in `wrangler.jsonc` that is
`https://gmail-mcp.<your-subdomain>.workers.dev/mcp`. Your subdomain is printed
by the deploy, and the trailing **`/mcp`** matters — it is the `path=` passed to
`http_app()`.

In Claude: **Settings → Connectors → Add custom connector**, paste the URL, and
add the `MCP_AUTH_TOKEN` value as header `Authorization: Bearer <token>`.

## The tool

```python
get_latest_email_from_sender(
    sender: str,                    # "ada@example.com", "example.com" or "Ada"
    include_body: bool = True,
    max_body_chars: int = 4000,
    query_extra: str | None = None, # e.g. "is:unread", "newer_than:7d"
)
```

Returns `found`, `id`, `thread_id`, `from`, `to`, `subject`, `date`, `snippet`,
`label_ids`, and when requested `body` / `body_truncated`. Bodies prefer
`text/plain` and fall back to de-tagged `text/html`.

When the mailbox holds nothing from that sender it returns
`{"found": false, ...}` rather than raising — "no mail from this person" is an
answer, not a failure.

## Local development

```bash
uvx --from workers-py pywrangler dev
```

Then check the gate is closed and the handshake works:

```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST localhost:8787/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
# => 401

curl -s -X POST localhost:8787/mcp \
  -H "Authorization: Bearer $MCP_AUTH_TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

## Two Workers constraints this code is shaped by

**`stateless_http=True` is required.** Cloudflare's ASGI adapter drives a full
lifespan startup/shutdown cycle around *every request*, so nothing survives
between calls. A stateful MCP session would be destroyed the moment it was
created.

**Secrets arrive on the ASGI scope, not `os.environ`.** Worker bindings are
attached as `scope["env"]`, so the tool reads config off the current request via
`get_http_request()`. `envcfg` falls back to `os.environ` so the same code runs
under uvicorn locally.

## The `watchfiles` override

`pyproject.toml` overrides two of FastMCP's `server` extras out of the build:

- `watchfiles` — a Rust filesystem watcher used by `fastmcp dev` for hot reload.
  It has no WebAssembly wheel, and a Worker has no filesystem to watch.
- `pyperclip` — clipboard helper for the local CLI. A Worker has no clipboard.

Neither is imported on the request path; `mcp.http_app()` builds and serves
correctly with both absent. Without the override, `pywrangler sync` would try to
build `watchfiles` from source for wasm under `--no-build` and fail.

After the override the only packages still needing native wasm wheels are
`pydantic-core`, `rpds-py`, `cryptography`, `cffi` and `pyyaml` — all standard
Pyodide-bundled packages.
