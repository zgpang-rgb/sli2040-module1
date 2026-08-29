"""The MCP server and its single tool."""

from __future__ import annotations

from typing import Any

import gmail
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request

mcp: FastMCP = FastMCP(
    name="gmail-latest-email",
    instructions=(
        "Read-only access to a single Gmail mailbox. Use "
        "get_latest_email_from_sender to fetch the most recent message from a "
        "given sender."
    ),
)


@mcp.tool
async def get_latest_email_from_sender(
    sender: str,
    include_body: bool = True,
    max_body_chars: int = 4000,
    query_extra: str | None = None,
) -> dict[str, Any]:
    """Fetch the most recent email received from a given sender.

    Args:
        sender: Who the mail is from. A full address ("ada@example.com"), a
            domain ("example.com") or a display-name fragment ("Ada") all work;
            the value is passed to Gmail search as `from:<sender>`.
        include_body: Include the decoded message body. Set False when only the
            subject, date and snippet are needed.
        max_body_chars: Truncate the body at this many characters.
        query_extra: Additional raw Gmail search terms ANDed with the sender,
            e.g. "is:unread" or "newer_than:7d".

    Returns:
        The message as a flat dict with `found`, `id`, `thread_id`, `from`,
        `to`, `subject`, `date`, `snippet`, `label_ids` and (when requested)
        `body` / `body_truncated`. When the mailbox holds nothing from that
        sender, `found` is False and `message` explains — that is a normal
        result, not an error.
    """
    # Worker secrets arrive on the ASGI scope, so the tool has to reach the
    # current request to read them.
    scope = get_http_request().scope

    access_token = await gmail.get_access_token(scope)
    message_id = await gmail.find_latest_message_id(access_token, sender, query_extra)

    if message_id is None:
        return {
            "found": False,
            "sender": sender,
            "message": f"No message from {sender!r} was found in this mailbox.",
        }

    message = await gmail.get_message(access_token, message_id)
    return gmail.summarize(
        message, include_body=include_body, max_body_chars=max_body_chars
    )
