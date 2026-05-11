from urllib.parse import urlencode

from app.integrations.twitch.client import post_form
from app.integrations.twitch.config import (
    TWITCH_AUTH_BASE_URL,
    TWITCH_CLIENT_ID,
    TWITCH_CLIENT_SECRET,
    TWITCH_REDIRECT_URI,
    TWITCH_SCOPES,
)


def build_auth_url(state: str = "default_state") -> str:
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "redirect_uri": TWITCH_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(TWITCH_SCOPES),
        "state": state,
    }
    return f"{TWITCH_AUTH_BASE_URL}/authorize?{urlencode(params)}"


async def exchange_code_for_token(code: str) -> dict:
    payload = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": TWITCH_REDIRECT_URI,
    }
    return await post_form(f"{TWITCH_AUTH_BASE_URL}/token", data=payload)
