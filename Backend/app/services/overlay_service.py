import secrets

from fastapi import HTTPException

from app.database import supabase

DEFAULT_STATE = "idle"


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


def _ensure_twitch_connected(user_id: str) -> None:
    channel = (
        supabase.table("twitch_channels")
        .select("id")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    if not channel.data:
        raise HTTPException(status_code=400, detail="Debes vincular Twitch antes de generar tu URL de OBS.")


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

    profile_resp = (
        supabase.table("user_profiles")
        .select("user_id,overlay_token")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    if not profile_resp.data:
        raise HTTPException(status_code=404, detail="Perfil de usuario no encontrado")

    profile = profile_resp.data[0]
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

    profile_resp = (
        supabase.table("user_profiles")
        .select("user_id,overlay_token")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    if not profile_resp.data:
        raise HTTPException(status_code=404, detail="Perfil de usuario no encontrado")

    old_token = profile_resp.data[0].get("overlay_token")
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
    response = (
        supabase.table("overlay_states")
        .select("overlay_token,current_state,payload,updated_at")
        .eq("overlay_token", overlay_token)
        .limit(1)
        .execute()
    )

    rows = response.data or []
    if rows:
        return _serialize(rows[0])

    created = (
        supabase.table("overlay_states")
        .insert({"overlay_token": overlay_token, "current_state": DEFAULT_STATE, "payload": {}})
        .execute()
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

    response = (
        supabase.table("overlay_states")
        .upsert(data, on_conflict="overlay_token")
        .execute()
    )
    rows = response.data or [data]
    return _serialize(rows[0])


def hide_overlay(overlay_token: str) -> dict:
    return update_overlay_state(
        overlay_token=overlay_token,
        current_state="hidden",
        payload={},
    )
