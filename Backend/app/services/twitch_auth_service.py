from datetime import datetime, timezone

from fastapi import HTTPException

from app.database import supabase
from app.integrations.twitch.auth import build_auth_url, exchange_code_for_token
from app.integrations.twitch.client import get_json
from app.integrations.twitch.config import (
    TWITCH_API_BASE_URL,
    TWITCH_CLIENT_ID,
    TWITCH_REDIRECT_URI,
)


TWITCH_CHANNELS_TABLE = "twitch_channels"


def get_auth_url() -> str:
    if not TWITCH_CLIENT_ID or not TWITCH_REDIRECT_URI:
        raise HTTPException(status_code=400, detail="Missing TWITCH_CLIENT_ID or TWITCH_REDIRECT_URI")
    return build_auth_url()


async def _fetch_twitch_user(access_token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Client-Id": TWITCH_CLIENT_ID or "",
    }
    payload = await get_json(f"{TWITCH_API_BASE_URL}/users", headers=headers)
    users = payload.get("data", [])
    if not users:
        raise HTTPException(status_code=400, detail="No se pudo obtener el usuario de Twitch.")
    return users[0]


def _to_channel_data(user: dict) -> dict:
    return {
        "twitch_user_id": user.get("id", ""),
        "login": user.get("login", ""),
        "display_name": user.get("display_name", ""),
        "email": user.get("email"),
        "profile_image_url": user.get("profile_image_url"),
    }


def _upsert_twitch_channel(*, user: dict, token_payload: dict) -> None:
    now_iso = datetime.now(timezone.utc).isoformat()
    db_payload = {
        "twitch_user_id": user.get("id"),
        "login": user.get("login"),
        "display_name": user.get("display_name"),
        "email": user.get("email"),
        "profile_image_url": user.get("profile_image_url"),
        "access_token": token_payload.get("access_token"),
        "refresh_token": token_payload.get("refresh_token"),
        "token_type": token_payload.get("token_type"),
        "expires_in": token_payload.get("expires_in"),
        "scopes": token_payload.get("scope", []),
        "connected_at": now_iso,
        "updated_at": now_iso,
    }

    existing = (
        supabase.table(TWITCH_CHANNELS_TABLE)
        .select("id")
        .eq("twitch_user_id", user.get("id"))
        .limit(1)
        .execute()
    )

    if existing.data:
        (
            supabase.table(TWITCH_CHANNELS_TABLE)
            .update(db_payload)
            .eq("twitch_user_id", user.get("id"))
            .execute()
        )
        return

    supabase.table(TWITCH_CHANNELS_TABLE).insert(db_payload).execute()


async def handle_twitch_callback(code: str | None) -> dict:
    if not code:
        return {
            "connected": False,
            "message": "Falta el parámetro 'code' en el callback de Twitch.",
            "channel": None,
            "token_saved": False,
        }

    token_payload = await exchange_code_for_token(code)
    access_token = token_payload.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="No se recibió access token desde Twitch.")

    user = await _fetch_twitch_user(access_token)
    _upsert_twitch_channel(user=user, token_payload=token_payload)

    return {
        "connected": True,
        "message": "Canal de Twitch conectado correctamente.",
        "channel": _to_channel_data(user),
        "token_saved": True,
    }


async def get_me(access_token: str | None = None) -> dict:
    if access_token:
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Client-Id": TWITCH_CLIENT_ID or "",
            }
            return await get_json(f"{TWITCH_API_BASE_URL}/users", headers=headers)
        except Exception:
            return {"data": []}

    stored_channel = (
        supabase.table(TWITCH_CHANNELS_TABLE)
        .select("twitch_user_id, login, display_name, email, profile_image_url")
        .order("updated_at", desc=True)
        .limit(1)
        .execute()
    )

    if stored_channel.data:
        channel = stored_channel.data[0]
        return {
            "connected": True,
            "message": "Canal de Twitch conectado.",
            "channel": {
                "twitch_user_id": channel.get("twitch_user_id", ""),
                "login": channel.get("login", ""),
                "display_name": channel.get("display_name", ""),
                "email": channel.get("email"),
                "profile_image_url": channel.get("profile_image_url"),
            },
        }

    return {
        "connected": False,
        "message": "No hay canal de Twitch conectado todavía.",
        "channel": None,
    }


async def disconnect_channel() -> dict:
    existing = (
        supabase.table(TWITCH_CHANNELS_TABLE)
        .select("id")
        .order("updated_at", desc=True)
        .limit(1)
        .execute()
    )

    if not existing.data:
        return {
            "connected": False,
            "message": "No había un canal de Twitch vinculado.",
            "channel": None,
        }

    channel_id = existing.data[0].get("id")
    if channel_id:
        supabase.table(TWITCH_CHANNELS_TABLE).delete().eq("id", channel_id).execute()

    return {
        "connected": False,
        "message": "Canal de Twitch desvinculado correctamente.",
        "channel": None,
    }
