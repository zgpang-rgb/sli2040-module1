"""Gmail REST client: exchange a refresh token, then find and read one message.

Deliberately no Google SDK. The official client libraries assume a filesystem,
threads and a socket-based transport, none of which a Worker provides; three
plain HTTPS calls do the whole job.

Required OAuth scope: https://www.googleapis.com/auth/gmail.readonly
"""

from __future__ import annotations

import base64
import binascii
import re
from typing import Any

import envcfg
from http_client import request_json

TOKEN_URL = "https://oauth2.googleapis.com/token"
GMAIL_API = "https://gmail.googleapis.com/gmail/v1/users/me"

_HTML_BLOCK_TAGS = re.compile(r"(?i)</(?:p|div|tr|li|h[1-6]|blockquote)>|<br\s*/?>")
_HTML_TAGS = re.compile(r"(?s)<[^>]+>")
_HTML_DROP = re.compile(r"(?is)<(script|style)\b.*?</\1>")
_BLANK_LINES = re.compile(r"\n{3,}")


async def get_access_token(scope: dict[str, Any] | None) -> str:
    """Exchange the stored refresh token for a short-lived access token."""
    payload = await request_json(
        "POST",
        TOKEN_URL,
        form={
            "client_id": envcfg.require(scope, "GOOGLE_CLIENT_ID"),
            "client_secret": envcfg.require(scope, "GOOGLE_CLIENT_SECRET"),
            "refresh_token": envcfg.require(scope, "GMAIL_REFRESH_TOKEN"),
            "grant_type": "refresh_token",
        },
    )
    token = payload.get("access_token")
    if not token:
        raise RuntimeError(f"Google returned no access_token: {payload}")
    return str(token)


async def find_latest_message_id(
    access_token: str, sender: str, query_extra: str | None = None
) -> str | None:
    """Return the id of the most recent message from *sender*, or None."""
    # Gmail returns matches newest-first, so maxResults=1 is the latest message.
    query = f"from:{sender}"
    if query_extra:
        query = f"{query} {query_extra}"

    payload = await request_json(
        "GET",
        f"{GMAIL_API}/messages",
        params={"q": query, "maxResults": "1"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    messages = payload.get("messages") or []
    return str(messages[0]["id"]) if messages else None


async def get_message(access_token: str, message_id: str) -> dict[str, Any]:
    """Fetch one message in full form."""
    return await request_json(
        "GET",
        f"{GMAIL_API}/messages/{message_id}",
        params={"format": "full"},
        headers={"Authorization": f"Bearer {access_token}"},
    )


def _headers_to_dict(payload: dict[str, Any]) -> dict[str, str]:
    return {
        str(h.get("name", "")).lower(): str(h.get("value", ""))
        for h in payload.get("headers") or []
    }


def _decode_part(data: str) -> str:
    """Decode Gmail's base64url body data, tolerating missing padding."""
    try:
        raw = base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))
    except (binascii.Error, ValueError):
        return ""
    return raw.decode("utf-8", errors="replace")


def _html_to_text(html: str) -> str:
    text = _HTML_DROP.sub("", html)
    text = _HTML_BLOCK_TAGS.sub("\n", text)
    text = _HTML_TAGS.sub("", text)
    for entity, char in (
        ("&nbsp;", " "),
        ("&amp;", "&"),
        ("&lt;", "<"),
        ("&gt;", ">"),
        ("&quot;", '"'),
        ("&#39;", "'"),
    ):
        text = text.replace(entity, char)
    return _BLANK_LINES.sub("\n\n", text).strip()


def extract_body(payload: dict[str, Any]) -> str:
    """Walk the MIME tree and return the best available plain-text body.

    Prefers a real text/plain part; falls back to de-tagged text/html, which is
    all many marketing senders provide.
    """
    plain: list[str] = []
    html: list[str] = []

    def walk(part: dict[str, Any]) -> None:
        mime = str(part.get("mimeType", ""))
        data = (part.get("body") or {}).get("data")
        if data:
            if mime == "text/plain":
                plain.append(_decode_part(data))
            elif mime == "text/html":
                html.append(_decode_part(data))
        for child in part.get("parts") or []:
            walk(child)

    walk(payload)

    if plain:
        return "\n".join(plain).strip()
    if html:
        return _html_to_text("\n".join(html))
    return ""


def summarize(
    message: dict[str, Any], *, include_body: bool, max_body_chars: int
) -> dict[str, Any]:
    """Reduce a raw Gmail message into the flat shape the tool returns."""
    payload = message.get("payload") or {}
    headers = _headers_to_dict(payload)

    result: dict[str, Any] = {
        "found": True,
        "id": message.get("id"),
        "thread_id": message.get("threadId"),
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "subject": headers.get("subject", ""),
        "date": headers.get("date", ""),
        "snippet": message.get("snippet", ""),
        "label_ids": message.get("labelIds") or [],
    }

    if include_body:
        body = extract_body(payload)
        truncated = len(body) > max_body_chars
        result["body"] = body[:max_body_chars]
        result["body_truncated"] = truncated

    return result
