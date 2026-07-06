"""Push team announcements to Slack. Best-effort: never blocks pinning in the Hub."""

from __future__ import annotations

import streamlit as st


def _slack_secrets() -> dict:
    try:
        return dict(st.secrets["slack"])
    except (KeyError, FileNotFoundError):
        return {}


def post_announcement(text: str) -> tuple[bool, str | None]:
    """Post a pinned announcement to the configured Slack channel.

    Returns (ok, error_message). No-ops quietly if bot_token/announcement_channel
    aren't configured, since Slack push is optional on top of the Hub banner.
    """
    cfg = _slack_secrets()
    token = cfg.get("bot_token")
    channel = cfg.get("announcement_channel")
    if not token or not channel:
        return False, None

    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError

    client = WebClient(token=token)
    try:
        client.chat_postMessage(channel=channel, text=f":pushpin: *Team announcement*\n{text}")
        return True, None
    except SlackApiError as e:
        return False, e.response.get("error", str(e))
