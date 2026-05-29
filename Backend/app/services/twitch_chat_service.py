from datetime import datetime, timezone

import httpx
from fastapi import HTTPException
from postgrest.exceptions import APIError

from app.database import supabase
from app.services.audit_service import create_audit_log
from app.services.participant_service import normalize_username
from app.services.supabase_retry import RETRYABLE_SUPABASE_ERRORS, execute_with_retry

PROCESSABLE_RAFFLE_STATUSES = ["draft", "active", "pending_claim"]
RETRYABLE_ERRORS = RETRYABLE_SUPABASE_ERRORS


def _normalized_text(value: str | None) -> str:
    return (value or "").strip().lower()



def _is_duplicate_source_event_error(error: APIError) -> bool:
    error_code = str(getattr(error, "code", ""))
    message = str(error).lower()
    return (
        error_code == "23505"
        or "uq_participation_entries_source_event_id" in message
        or ("duplicate key" in message and "source_event_id" in message)
    )

def _safe_supabase(query):
    try:
        return execute_with_retry(query)
    except RETRYABLE_ERRORS as error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo procesar temporalmente el mensaje de chat. Inténtalo nuevamente.",
        ) from error


def _resolve_user_channel(user_id: str) -> dict:
    channel_response = _safe_supabase(
        supabase.table("twitch_channels")
        .select("id,user_id,twitch_user_id")
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .limit(1)
    )
    channels = channel_response.data or []
    if not channels:
        raise HTTPException(status_code=400, detail="No hay canal de Twitch vinculado para procesar mensajes.")
    return channels[0]


def _resolve_latest_processible_raffle(channel_id: str) -> dict:
    raffle_response = _safe_supabase(
        supabase.table("raffles")
        .select("id,command,status,channel_id,created_at,updated_at")
        .eq("channel_id", channel_id)
        .in_("status", PROCESSABLE_RAFFLE_STATUSES)
        .order("updated_at", desc=True)
        .order("created_at", desc=True)
        .limit(1)
    )
    raffles = raffle_response.data or []
    if not raffles:
        raise HTTPException(status_code=404, detail="No hay sorteo activo para procesar el mensaje.")
    return raffles[0]


def _get_or_create_participant(twitch_user_id: str, username: str, display_name: str | None) -> dict:
    normalized_username = normalize_username(username)
    participant = None

    by_twitch = _safe_supabase(supabase.table("participants").select("*").eq("twitch_user_id", twitch_user_id).limit(1))
    if by_twitch.data:
        participant = by_twitch.data[0]

    if not participant:
        by_username = _safe_supabase(supabase.table("participants").select("*").eq("username", normalized_username).limit(1))
        if by_username.data:
            participant = by_username.data[0]

    if participant:
        updates = {}
        if participant.get("username") != normalized_username:
            updates["username"] = normalized_username
        if display_name and participant.get("display_name") != display_name:
            updates["display_name"] = display_name
        if twitch_user_id and participant.get("twitch_user_id") != twitch_user_id:
            updates["twitch_user_id"] = twitch_user_id
        if updates:
            updated = _safe_supabase(supabase.table("participants").update(updates).eq("id", participant["id"]))
            if updated.data:
                participant = updated.data[0]
        return participant

    created = _safe_supabase(
        supabase.table("participants")
        .insert(
            {
                "twitch_user_id": twitch_user_id,
                "username": normalized_username,
                "display_name": display_name or normalized_username,
            }
        )
    )
    return created.data[0]


def process_chat_message(*, streamer_user_id: str, message_id: str, twitch_user_id: str, username: str, display_name: str | None, message_text: str) -> dict:
    if not message_id.strip():
        raise HTTPException(status_code=400, detail="message_id es obligatorio.")
    if not message_text.strip():
        raise HTTPException(status_code=400, detail="message_text no debe estar vacío.")

    channel = _resolve_user_channel(streamer_user_id)
    raffle = _resolve_latest_processible_raffle(channel["id"])

    duplicate_entry = _safe_supabase(
        supabase.table("participation_entries")
        .select("id")
        .eq("source_event_id", message_id)
        .limit(1)
    )
    if duplicate_entry.data:
        return {"message": "Mensaje ya procesado previamente", "data": {"duplicate_event": True}}

    participant = _get_or_create_participant(twitch_user_id=twitch_user_id, username=username, display_name=display_name)

    is_command = _normalized_text(message_text) == _normalized_text(raffle.get("command"))

    try:
        _safe_supabase(
            supabase.table("chat_messages")
            .insert(
                {
                    "raffle_id": raffle["id"],
                    "participant_id": participant["id"],
                    "message_text": message_text,
                    "is_command": is_command,
                    "sent_at": datetime.now(timezone.utc).isoformat(),
                }
            )
        )
    except APIError as error:
        message = str(error).lower()
        if str(getattr(error, "code", "")) == "23505" or ("duplicate key" in message and "chat_messages" in message):
            return {"message": "Mensaje ya procesado previamente", "data": {"duplicate_event": True}}
        raise

    participant_registered = False
    entry_created = False

    if is_command:
        existing_link = _safe_supabase(
            supabase.table("raffle_participants")
            .select("id")
            .eq("raffle_id", raffle["id"])
            .eq("participant_id", participant["id"])
            .limit(1)
        )

        if not existing_link.data:
            _safe_supabase(
                supabase.table("raffle_participants")
                .insert(
                    {
                        "raffle_id": raffle["id"],
                        "participant_id": participant["id"],
                        "entry_source": "chat_command",
                        "status": "registered",
                        "is_eligible": False,
                        "final_score": 0,
                    }
                )
            )
            participant_registered = True

        existing_entry = _safe_supabase(
            supabase.table("participation_entries")
            .select("id")
            .eq("source_event_id", message_id)
            .limit(1)
        )
        if not existing_entry.data:
            try:
                _safe_supabase(
                    supabase.table("participation_entries")
                    .insert(
                        {
                            "raffle_id": raffle["id"],
                            "participant_id": participant["id"],
                            "entry_type": "chat_command",
                            "source_event_id": message_id,
                            "content": message_text,
                        }
                    )
                )
                entry_created = True
            except APIError as error:
                if _is_duplicate_source_event_error(error):
                    return {"message": "Mensaje ya procesado previamente", "data": {"duplicate_event": True}}
                raise

        if participant_registered:
            try:
                create_audit_log(
                    raffle_id=raffle["id"],
                    participant_id=participant["id"],
                    action="chat_command_entry",
                    detail="Participante registrado por comando de chat",
                )
            except RETRYABLE_ERRORS as error:
                raise HTTPException(
                    status_code=503,
                    detail="No se pudo procesar temporalmente el mensaje de chat. Inténtalo nuevamente.",
                ) from error

    return {
        "message": "Mensaje procesado correctamente",
        "data": {
            "raffle_id": raffle["id"],
            "participant_id": participant["id"],
            "username": participant.get("username"),
            "is_command": is_command,
            "participant_registered": participant_registered,
            "entry_created": entry_created,
            "duplicate_event": False,
        },
    }


def process_test_message(*, user_id: str, message_id: str, twitch_user_id: str, username: str, display_name: str | None, message_text: str) -> dict:
    return process_chat_message(
        streamer_user_id=user_id,
        message_id=message_id,
        twitch_user_id=twitch_user_id,
        username=username,
        display_name=display_name,
        message_text=message_text,
    )
