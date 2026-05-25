import secrets
import logging
import time

import httpx
from fastapi import HTTPException

from app.database import supabase

DEFAULT_STATE = "idle"
logger = logging.getLogger(__name__)


class OverlayStorageUnavailable(Exception):
    pass


def generate_overlay_token() -> str:
    return secrets.token_urlsafe(32)


def _serialize(row: dict) -> dict:
    return {
        "overlay_token": row.get("overlay_token"),
        "current_state": row.get("current_state", DEFAULT_STATE),
        "payload": row.get("payload") or {},
        "updated_at": row.get("updated_at"),
    }


def _build_overlay_url(frontend_base_url: str, overlay_token: str) -> str:
    return f"{frontend_base_url.rstrip('/')}/overlay/{overlay_token}"


def _is_temporary_connection_error(error: Exception) -> bool:
    transient_types = (
        httpx.RemoteProtocolError,
        httpx.ConnectError,
        httpx.ReadTimeout,
        httpx.TimeoutException,
    )
    if isinstance(error, transient_types):
        return True

    cause = getattr(error, "__cause__", None)
    if isinstance(cause, transient_types):
        return True

    message = str(error).lower()
    return "server disconnected" in message or "connection" in message or "timeout" in message


def execute_with_retry(query, *, retries: int = 2, delay: float = 0.3, operation: str = "query"):
    attempts = retries + 1
    for attempt in range(1, attempts + 1):
        try:
            return query.execute()
        except Exception as error:
            temporary = _is_temporary_connection_error(error)
            logger.exception("[overlay] Supabase connection error while %s", operation)

            if not temporary:
                raise

            if attempt >= attempts:
                logger.error("[overlay] Supabase unavailable after retries")
                raise OverlayStorageUnavailable() from error

            logger.warning("[overlay] Retrying Supabase query... (%s/%s)", attempt, attempts)
            time.sleep(delay)


def _ensure_twitch_connected(user_id: str) -> None:
    logger.info("/overlay/me auth user_id=%s", user_id)
    channel = (
        supabase.table("twitch_channels")
        .select("id,twitch_user_id,login,display_name,updated_at")
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .limit(1)
        .execute()
    )
    channel_rows = channel.data or []
    logger.info("/overlay/me twitch lookup rows=%s", channel_rows)
    if not channel_rows:
        logger.warning("/overlay/me rejected: no connected twitch channel found")
        raise HTTPException(status_code=400, detail="Debes vincular Twitch antes de generar tu URL de OBS.")


def _get_or_create_user_profile(user_id: str) -> dict:
    profile_resp = (
        supabase.table("user_profiles")
        .select("user_id,overlay_token")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    rows = profile_resp.data or []
    logger.info("/overlay/me user_profiles lookup rows=%s", rows)

    if rows:
        return rows[0]

    created = (
        supabase.table("user_profiles")
        .insert({"user_id": user_id})
        .execute()
    )
    created_rows = created.data or [{"user_id": user_id, "overlay_token": None}]
    logger.info("/overlay/me user_profile created=%s", created_rows[0])
    return created_rows[0]


def _upsert_idle_overlay_state(overlay_token: str, streamer_id: str | None = None) -> None:
    payload = {
        "overlay_token": overlay_token,
        "current_state": DEFAULT_STATE,
        "payload": {},
    }
    if streamer_id is not None:
        payload["streamer_id"] = streamer_id
    supabase.table("overlay_states").upsert(payload, on_conflict="overlay_token").execute()


def get_or_create_user_overlay(user_id: str, frontend_base_url: str) -> dict:
    _ensure_twitch_connected(user_id)

    profile = _get_or_create_user_profile(user_id)
    overlay_token = profile.get("overlay_token")

    if not overlay_token:
        overlay_token = generate_overlay_token()
        (
            supabase.table("user_profiles")
            .update({"overlay_token": overlay_token})
            .eq("user_id", user_id)
            .execute()
        )

    _upsert_idle_overlay_state(overlay_token, user_id)

    return {
        "overlay_token": overlay_token,
        "overlay_url": _build_overlay_url(frontend_base_url, overlay_token),
    }


def regenerate_user_overlay(user_id: str, frontend_base_url: str) -> dict:
    _ensure_twitch_connected(user_id)

    profile = _get_or_create_user_profile(user_id)
    old_token = profile.get("overlay_token")
    new_token = generate_overlay_token()

    (
        supabase.table("user_profiles")
        .update({"overlay_token": new_token})
        .eq("user_id", user_id)
        .execute()
    )

    _upsert_idle_overlay_state(new_token, user_id)

    if old_token:
        hide_overlay(old_token)

    return {
        "overlay_token": new_token,
        "overlay_url": _build_overlay_url(frontend_base_url, new_token),
    }


def get_overlay_state(overlay_token: str) -> dict:
    response = execute_with_retry(
        supabase.table("overlay_states")
        .select("overlay_token,current_state,payload,updated_at")
        .eq("overlay_token", overlay_token)
        .limit(1),
        operation="reading state",
    )

    rows = response.data or []
    if rows:
        return _serialize(rows[0])

    created = execute_with_retry(
        supabase.table("overlay_states")
        .insert({"overlay_token": overlay_token, "current_state": DEFAULT_STATE, "payload": {}}),
        operation="creating default state",
    )
    created_rows = created.data or [{"overlay_token": overlay_token, "current_state": DEFAULT_STATE, "payload": {}, "updated_at": None}]
    return _serialize(created_rows[0])


def update_overlay_state(
    overlay_token: str,
    current_state: str,
    payload: dict,
    streamer_id: str | None = None,
) -> dict:
    data = {
        "overlay_token": overlay_token,
        "current_state": current_state,
        "payload": payload or {},
    }
    if streamer_id is not None:
        data["streamer_id"] = streamer_id

    response = execute_with_retry(
        supabase.table("overlay_states")
        .upsert(data, on_conflict="overlay_token"),
        operation="updating state",
    )
    rows = response.data or [data]
    return _serialize(rows[0])


def hide_overlay(overlay_token: str) -> dict:
    return update_overlay_state(
        overlay_token=overlay_token,
        current_state="hidden",
        payload={},
    )
