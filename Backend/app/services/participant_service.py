from datetime import datetime, timezone

import httpx
from fastapi import HTTPException
from postgrest.exceptions import APIError

from app.database import supabase
from app.schemas.enums import EntrySource
from app.services.supabase_retry import RETRYABLE_SUPABASE_ERRORS, execute_with_retry


def normalize_username(username: str) -> str:
    return username.strip().lower().replace(" ", "_")


def _safe_supabase(query, detail: str = "No se pudo completar la operación temporalmente. Inténtalo nuevamente."):
    try:
        return execute_with_retry(query)
    except RETRYABLE_SUPABASE_ERRORS as error:
        raise HTTPException(status_code=503, detail=detail) from error


def _entry_source_value(entry_source: EntrySource | str) -> str:
    return entry_source.value if isinstance(entry_source, EntrySource) else str(entry_source)


def _is_duplicate_source_event_error(error: APIError) -> bool:
    error_code = str(getattr(error, "code", ""))
    message = str(error).lower()
    return (
        error_code == "23505"
        or "uq_participation_entries_source_event_id" in message
        or ("duplicate key" in message and "source_event_id" in message)
    )


def _is_duplicate_raffle_participant_error(error: APIError) -> bool:
    error_code = str(getattr(error, "code", ""))
    message = str(error).lower()
    return (
        error_code == "23505"
        or "raffle_participants_raffle_id_participant_id_key" in message
        or ("duplicate key" in message and "raffle_participants" in message)
    )


def _validate_active_raffle(raffle_id: str) -> dict:
    raffle_response = _safe_supabase(
        supabase.table("raffles").select("*").eq("id", raffle_id).single(),
        "No se pudo validar temporalmente el sorteo. Inténtalo nuevamente.",
    )
    raffle = raffle_response.data

    if not raffle:
        raise HTTPException(status_code=404, detail="Sorteo no encontrado.")
    if raffle["status"] != "active":
        raise HTTPException(status_code=400, detail="Solo se pueden registrar participantes en sorteos activos.")
    return raffle


def upsert_participant(
    raffle_id: str,
    username: str,
    display_name: str | None = None,
    twitch_user_id: str | None = None,
    entry_source: EntrySource | str = EntrySource.chat_command,
    entry_content: str | None = None,
    source_event_id: str | None = None,
):
    retry_detail = "No se pudo registrar temporalmente el participante. Inténtalo nuevamente."
    raffle = _validate_active_raffle(raffle_id)

    if source_event_id:
        existing_entry = _safe_supabase(
            supabase.table("participation_entries")
            .select("*")
            .eq("source_event_id", source_event_id)
            .limit(1),
            retry_detail,
        )
        if existing_entry.data:
            return {
                "raffle": raffle,
                "participant": None,
                "entry": existing_entry.data[0],
                "duplicate": True,
            }

    username = normalize_username(username)
    display_name = display_name or username
    existing = _safe_supabase(
        supabase.table("participants").select("*").eq("username", username).limit(1),
        retry_detail,
    )
    if existing.data:
        participant = existing.data[0]
    else:
        created_participant = _safe_supabase(
            supabase.table("participants").insert(
                {"twitch_user_id": twitch_user_id, "username": username, "display_name": display_name}
            ),
            retry_detail,
        )
        participant = created_participant.data[0]

    existing_link = _safe_supabase(
        supabase.table("raffle_participants")
        .select("*")
        .eq("raffle_id", raffle_id)
        .eq("participant_id", participant["id"]),
        retry_detail,
    )
    if not existing_link.data:
        try:
            _safe_supabase(
                supabase.table("raffle_participants").insert(
                    {
                        "raffle_id": raffle_id,
                        "participant_id": participant["id"],
                        "entry_source": _entry_source_value(entry_source),
                        "status": "registered",
                    }
                ),
                retry_detail,
            )
        except APIError as error:
            if not _is_duplicate_raffle_participant_error(error):
                raise
            existing_link = _safe_supabase(
                supabase.table("raffle_participants")
                .select("*")
                .eq("raffle_id", raffle_id)
                .eq("participant_id", participant["id"])
                .limit(1),
                retry_detail,
            )

    if not entry_content:
        if entry_source == EntrySource.chat_command or entry_source == EntrySource.chat_command.value:
            entry_content = raffle.get("command", "!sorteo")
        elif entry_source == EntrySource.manual or entry_source == EntrySource.manual.value:
            entry_content = "Participante agregado manualmente por el streamer."
        elif entry_source == EntrySource.channel_points_reward or entry_source == EntrySource.channel_points_reward.value:
            entry_content = "Participante ingresó mediante canje de recompensa."
        else:
            entry_content = "Participante ingresó al sorteo."

    try:
        entry_response = _safe_supabase(
            supabase.table("participation_entries").insert(
                {
                    "raffle_id": raffle_id,
                    "participant_id": participant["id"],
                    "entry_type": _entry_source_value(entry_source),
                    "source_event_id": source_event_id,
                    "content": entry_content,
                }
            ),
            retry_detail,
        )
    except APIError as error:
        if source_event_id and _is_duplicate_source_event_error(error):
            return {"raffle": raffle, "participant": participant, "entry": None, "duplicate": True}
        raise

    return {
        "raffle": raffle,
        "participant": participant,
        "entry": entry_response.data[0] if entry_response.data else None,
        "duplicate": False,
    }


def bulk_register_participants(raffle_id: str, participants: list[dict]):
    _validate_active_raffle(raffle_id)

    normalized_payload = []
    seen_usernames = set()
    for item in participants:
        normalized_username = normalize_username(item["username"])
        if not normalized_username or normalized_username in seen_usernames:
            continue
        seen_usernames.add(normalized_username)
        normalized_payload.append({
            "username": normalized_username,
            "display_name": item.get("display_name") or normalized_username,
            "twitch_user_id": item.get("twitch_user_id"),
            "entry_source": item.get("entry_source", EntrySource.manual),
        })

    inserted_count = 0
    skipped_count = 0
    result_participants = []

    for item in normalized_payload:
        response = upsert_participant(
            raffle_id=raffle_id,
            username=item["username"],
            display_name=item["display_name"],
            twitch_user_id=item["twitch_user_id"],
            entry_source=item["entry_source"],
            entry_content="Participante agregado manualmente por carga masiva.",
        )

        if response.get("duplicate"):
            skipped_count += 1
            continue

        inserted_count += 1
        result_participants.append(response["participant"])

    return {
        "raffle_id": raffle_id,
        "inserted_count": inserted_count,
        "skipped_count": skipped_count + (len(participants) - len(normalized_payload)),
        "participants": result_participants,
    }


def list_raffle_participants(raffle_id: str):
    _validate_active_raffle(raffle_id)

    response = _safe_supabase(
        supabase.table("raffle_participants")
        .select("participant_id, entry_source, status, is_eligible, final_score, joined_at, participants:participant_id(username, display_name, twitch_user_id)")
        .eq("raffle_id", raffle_id)
        .neq("status", "removed")
        .order("joined_at", desc=False),
        "No se pudo obtener temporalmente la lista de participantes. Inténtalo nuevamente.",
    )

    data = []
    for item in response.data or []:
        participant = item.get("participants") or {}
        data.append({
            "participant_id": item.get("participant_id"),
            "username": participant.get("username"),
            "display_name": participant.get("display_name"),
            "twitch_user_id": participant.get("twitch_user_id"),
            "entry_source": item.get("entry_source"),
            "status": item.get("status"),
            "is_eligible": item.get("is_eligible"),
            "final_score": item.get("final_score"),
            "joined_at": item.get("joined_at"),
        })

    return {
        "message": "Participantes obtenidos correctamente",
        "data": data,
    }


def remove_participant_from_raffle(raffle_id: str, participant_id: str, reason: str | None = None):
    retry_detail = "No se pudo remover temporalmente el participante. Inténtalo nuevamente."
    _validate_active_raffle(raffle_id)

    relation_response = _safe_supabase(
        supabase.table("raffle_participants")
        .select("*")
        .eq("raffle_id", raffle_id)
        .eq("participant_id", participant_id)
        .limit(1),
        retry_detail,
    )

    if not relation_response.data:
        raise HTTPException(status_code=404, detail="Participante no encontrado en el sorteo.")

    relation = relation_response.data[0]
    if relation.get("status") == "removed":
        return {"message": "El participante ya estaba removido.", "raffle_participant": relation}

    payload = {
        "status": "removed",
        "removed_at": datetime.now(timezone.utc).isoformat(),
        "removal_reason": reason,
    }

    updated = _safe_supabase(
        supabase.table("raffle_participants").update(payload).eq("id", relation["id"]),
        retry_detail,
    )

    _safe_supabase(
        supabase.table("audit_logs").insert({
            "raffle_id": raffle_id,
            "participant_id": participant_id,
            "action": "participant_removed",
            "detail": reason or "Participante removido manualmente del sorteo.",
        }),
        retry_detail,
    )

    return {"message": "Participante removido correctamente.", "raffle_participant": updated.data[0] if updated.data else payload}


def register_participant_in_raffle(
    raffle_id: str,
    username: str,
    display_name: str | None = None,
    twitch_user_id: str | None = None,
    entry_source: EntrySource = EntrySource.chat_command,
    entry_content: str | None = None,
    source_event_id: str | None = None,
):
    return upsert_participant(
        raffle_id=raffle_id,
        username=username,
        display_name=display_name,
        twitch_user_id=twitch_user_id,
        entry_source=entry_source,
        entry_content=entry_content,
        source_event_id=source_event_id,
    )
