from datetime import datetime, timezone
from datetime import timedelta
import logging

from fastapi import HTTPException
import jwt

from app.config import settings
from app.database import supabase
from app.integrations.twitch.auth import build_auth_url, exchange_code_for_token
from app.integrations.twitch.client import get_json
from app.integrations.twitch.config import (
    TWITCH_API_BASE_URL,
    TWITCH_CLIENT_ID,
    TWITCH_REDIRECT_URI,
)


TWITCH_CHANNELS_TABLE = "twitch_channels"
OAUTH_STATE_TTL_MINUTES = 10
logger = logging.getLogger(__name__)


def _state_secret() -> str:
    secret = settings.supabase_service_role_key
    if not secret:
        raise HTTPException(status_code=500, detail="JWT secret no configurado")
    return secret


def _build_oauth_state(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=OAUTH_STATE_TTL_MINUTES)).timestamp()),
        "purpose": "twitch_oauth",
    }
    return jwt.encode(payload, _state_secret(), algorithm="HS256")


def _resolve_oauth_state(state: str | None) -> str:
    if not state:
        raise HTTPException(status_code=400, detail="Falta state en el callback de Twitch.")
    try:
        payload = jwt.decode(state, _state_secret(), algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=400, detail="State de OAuth inválido o expirado.") from exc
    if payload.get("purpose") != "twitch_oauth" or not payload.get("sub"):
        raise HTTPException(status_code=400, detail="State de OAuth inválido.")
    user_id = str(payload["sub"])
    logger.info("/twitch/callback oauth state resolved user_id=%s", user_id)
    return user_id


def get_auth_url(user_id: str) -> str:
    if not TWITCH_CLIENT_ID or not TWITCH_REDIRECT_URI:
        raise HTTPException(status_code=400, detail="Missing TWITCH_CLIENT_ID or TWITCH_REDIRECT_URI")
    return build_auth_url(_build_oauth_state(user_id))


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


def _upsert_twitch_channel(*, user_id: str, user: dict, token_payload: dict) -> dict:
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
        "user_id": user_id,
    }

    existing = (
        supabase.table(TWITCH_CHANNELS_TABLE)
        .select("id,user_id")
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .limit(1)
        .execute()
    )

    if existing.data:
        channel_id = existing.data[0].get("id")
        (
            supabase.table(TWITCH_CHANNELS_TABLE)
            .update(db_payload)
            .eq("id", channel_id)
            .execute()
        )
        logger.info("/twitch/callback twitch_channel updated id=%s user_id=%s", channel_id, user_id)
        return {"id": channel_id, "user_id": user_id}

    created = supabase.table(TWITCH_CHANNELS_TABLE).insert(db_payload).execute()
    row = (created.data or [{}])[0]
    logger.info("/twitch/callback twitch_channel created id=%s user_id=%s", row.get("id"), user_id)
    return {"id": row.get("id"), "user_id": user_id}


async def handle_twitch_callback(code: str | None, state: str | None) -> dict:
    if not code:
        return {
            "connected": False,
            "message": "Falta el parámetro 'code' en el callback de Twitch.",
            "channel": None,
            "token_saved": False,
        }

    user_id = _resolve_oauth_state(state)
    token_payload = await exchange_code_for_token(code)
    access_token = token_payload.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="No se recibió access token desde Twitch.")

    user = await _fetch_twitch_user(access_token)
    _upsert_twitch_channel(user_id=user_id, user=user, token_payload=token_payload)

    return {
        "connected": True,
        "message": "Canal de Twitch conectado correctamente.",
        "channel": _to_channel_data(user),
        "token_saved": True,
    }


async def get_me(*, user_id: str, access_token: str | None = None) -> dict:
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
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .limit(1)
        .execute()
    )
    logger.info("/twitch/me auth user_id=%s", user_id)
    logger.info("/twitch/me twitch lookup rows=%s", stored_channel.data or [])

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


async def disconnect_channel(*, user_id: str) -> dict:
    existing = (
        supabase.table(TWITCH_CHANNELS_TABLE)
        .select("id")
        .eq("user_id", user_id)
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
