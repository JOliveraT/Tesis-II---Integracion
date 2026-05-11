from fastapi import HTTPException

from app.database import supabase
from app.schemas.enums import EntrySource
from app.schemas.message_schema import CreateMessageRequest
from app.services.participant_service import upsert_participant


def _normalize_command(value: str | None) -> str:
    return (value or "").strip().lower()


def _get_channel_raffle_command(twitch_channel_id: str) -> str | None:
    channel = (
        supabase.table("twitch_channels")
        .select("raffle_command")
        .eq("twitch_user_id", twitch_channel_id)
        .limit(1)
        .execute()
    )
    if not channel.data:
        return None
    return channel.data[0].get("raffle_command")


def process_chat_command_participation(
    raffle_id: str,
    twitch_channel_id: str,
    username: str,
    message_text: str,
    *,
    display_name: str | None = None,
    twitch_user_id: str | None = None,
    source_event_id: str | None = None,
) -> dict:
    configured_command = _get_channel_raffle_command(twitch_channel_id)
    if not configured_command:
        return {"matched": False, "registered": False, "duplicate": False, "entry": None}

    if _normalize_command(message_text) != _normalize_command(configured_command):
        return {"matched": False, "registered": False, "duplicate": False, "entry": None}

    result = upsert_participant(
        raffle_id=raffle_id,
        username=username,
        display_name=display_name,
        twitch_user_id=twitch_user_id,
        entry_source=EntrySource.chat_command,
        entry_content=configured_command,
        source_event_id=source_event_id,
    )

    return {
        "matched": True,
        "registered": not result.get("duplicate", False),
        "duplicate": result.get("duplicate", False),
        "entry": result.get("entry"),
    }


def process_eventsub_participation_event(event_type: str, event_payload: dict) -> dict:
    """Normalize Twitch EventSub payload and route it to command participation logic."""
    broadcaster_user_id = event_payload.get("broadcaster_user_id")
    if not broadcaster_user_id:
        return {"matched": False, "registered": False, "duplicate": False, "entry": None}

    viewer_username = event_payload.get("user_login") or event_payload.get("chatter_user_login") or ""
    display_name = event_payload.get("user_name") or event_payload.get("chatter_user_name")
    viewer_twitch_user_id = event_payload.get("user_id") or event_payload.get("chatter_user_id")

    reward = event_payload.get("reward") or {}
    message_text = (
        event_payload.get("message", {}).get("text")
        or event_payload.get("user_input")
        or reward.get("title")
        or ""
    )

    source_event_id = event_payload.get("id") or (
        f"{event_type}:{broadcaster_user_id}:{viewer_twitch_user_id}:{message_text}"
    )

    raffle_id = event_payload.get("reward_id") or reward.get("id") or broadcaster_user_id

    return process_chat_command_participation(
        raffle_id=raffle_id,
        twitch_channel_id=broadcaster_user_id,
        username=viewer_username,
        message_text=message_text,
        display_name=display_name,
        twitch_user_id=viewer_twitch_user_id,
        source_event_id=source_event_id,
    )


def create_message(data: CreateMessageRequest):
    raffle_response = supabase.table("raffles").select("*").eq("id", data.raffle_id).single().execute()
    raffle = raffle_response.data

    if not raffle:
        raise HTTPException(status_code=404, detail="Sorteo no encontrado.")

    if raffle["status"] != "active":
        raise HTTPException(status_code=400, detail="Solo se pueden registrar mensajes en sorteos activos.")

    participant_result = supabase.table("participants").select("*").eq("username", data.participant_username).execute()
    if not participant_result.data:
        raise HTTPException(status_code=404, detail="Participante no encontrado. Regístralo primero.")

    participant = participant_result.data[0]
    is_command = data.content.strip().startswith("!")

    response = supabase.table("chat_messages").insert(
        {
            "raffle_id": data.raffle_id,
            "participant_id": participant["id"],
            "message_text": data.content,
            "is_command": is_command,
        }
    ).execute()

    return {
        "message": "Mensaje registrado correctamente",
        "data": response.data,
    }
