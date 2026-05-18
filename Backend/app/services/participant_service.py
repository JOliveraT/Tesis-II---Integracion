from datetime import datetime, timezone

from fastapi import HTTPException

from app.database import supabase
from app.schemas.enums import EntrySource


def normalize_username(username: str) -> str:
    return username.strip().lower().replace(" ", "_")


def _validate_active_raffle(raffle_id: str) -> dict:
    raffle_response = supabase.table("raffles").select("*").eq("id", raffle_id).single().execute()
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
    entry_source: EntrySource = EntrySource.chat_command,
    entry_content: str | None = None,
    source_event_id: str | None = None,
):
    raffle = _validate_active_raffle(raffle_id)

    if source_event_id:
        existing_entry = (
            supabase.table("participation_entries")
            .select("*")
            .eq("raffle_id", raffle_id)
            .eq("source_event_id", source_event_id)
            .limit(1)
            .execute()
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
    existing = supabase.table("participants").select("*").eq("username", username).limit(1).execute()
    participant = existing.data[0] if existing.data else supabase.table("participants").insert(
        {"twitch_user_id": twitch_user_id, "username": username, "display_name": display_name}
    ).execute().data[0]

    existing_link = (
        supabase.table("raffle_participants").select("*").eq("raffle_id", raffle_id).eq("participant_id", participant["id"]).execute()
    )
    if not existing_link.data:
        supabase.table("raffle_participants").insert(
            {
                "raffle_id": raffle_id,
                "participant_id": participant["id"],
                "entry_source": entry_source.value,
                "status": "registered",
            }
        ).execute()

    if not entry_content:
        if entry_source == EntrySource.chat_command:
            entry_content = raffle.get("command", "!sorteo")
        elif entry_source == EntrySource.manual:
            entry_content = "Participante agregado manualmente por el streamer."
        elif entry_source == EntrySource.channel_points_reward:
            entry_content = "Participante ingresó mediante canje de recompensa."
        else:
            entry_content = "Participante ingresó al sorteo."

    entry_response = supabase.table("participation_entries").insert(
        {
            "raffle_id": raffle_id,
            "participant_id": participant["id"],
            "entry_type": entry_source.value,
            "source_event_id": source_event_id,
            "content": entry_content,
        }
    ).execute()

    return {"raffle": raffle, "participant": participant, "entry": entry_response.data[0] if entry_response.data else None, "duplicate": False}


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


def remove_participant_from_raffle(raffle_id: str, participant_id: str, reason: str | None = None):
    _validate_active_raffle(raffle_id)

    relation_response = (
        supabase.table("raffle_participants")
        .select("*")
        .eq("raffle_id", raffle_id)
        .eq("participant_id", participant_id)
        .limit(1)
        .execute()
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

    updated = (
        supabase.table("raffle_participants")
        .update(payload)
        .eq("id", relation["id"])
        .execute()
    )

    supabase.table("audit_logs").insert({
        "raffle_id": raffle_id,
        "participant_id": participant_id,
        "action": "participant_removed",
        "detail": reason or "Participante removido manualmente del sorteo.",
    }).execute()

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
