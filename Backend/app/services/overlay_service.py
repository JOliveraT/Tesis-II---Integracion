from app.database import supabase

DEFAULT_STATE = "idle"


def _serialize(row: dict) -> dict:
    return {
        "overlay_token": row.get("overlay_token"),
        "current_state": row.get("current_state", DEFAULT_STATE),
        "payload": row.get("payload") or {},
        "updated_at": row.get("updated_at"),
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
