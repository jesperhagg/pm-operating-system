"""
Slack integration — stub that prints to stdout when no credentials are set.
Set SLACK_BOT_TOKEN and SLACK_CHANNEL env vars for real integration.
"""

import os


def _is_configured() -> bool:
    return bool(os.environ.get("SLACK_BOT_TOKEN"))


def post_message(text: str, channel: str | None = None) -> dict:
    """Post a message to Slack. Prints to stdout in mockup mode."""
    channel = channel or os.environ.get("SLACK_CHANNEL", "#pm-digest")
    if _is_configured():
        return _post_real(text, channel)
    return _post_mockup(text, channel)


def post_blocks(blocks: list, text: str = "", channel: str | None = None) -> dict:
    """Post a rich Block Kit message to Slack."""
    channel = channel or os.environ.get("SLACK_CHANNEL", "#pm-digest")
    if _is_configured():
        return _post_blocks_real(blocks, text, channel)
    return _post_mockup(f"[Block message]\n{text}", channel)


# --- Mockup ---

def _post_mockup(text: str, channel: str) -> dict:
    print(f"\n{'='*60}")
    print(f"[SLACK MOCKUP] → {channel}")
    print('='*60)
    print(text)
    print('='*60 + "\n")
    return {"ok": True, "channel": channel, "_mockup": True}


# --- Real stubs ---

def _post_real(text: str, channel: str) -> dict:
    try:
        from slack_sdk import WebClient
        client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        response = client.chat_postMessage(channel=channel, text=text)
        return {"ok": response["ok"], "ts": response["ts"], "channel": channel}
    except ImportError:
        raise ImportError("Install slack_sdk: pip install slack-sdk")


def _post_blocks_real(blocks: list, text: str, channel: str) -> dict:
    try:
        from slack_sdk import WebClient
        client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        response = client.chat_postMessage(channel=channel, text=text, blocks=blocks)
        return {"ok": response["ok"], "ts": response["ts"], "channel": channel}
    except ImportError:
        raise ImportError("Install slack_sdk: pip install slack-sdk")
