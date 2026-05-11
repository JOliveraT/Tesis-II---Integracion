from fastapi import HTTPException

from app.database import supabase
from app.schemas.enums import EntrySource


def upsert_participant(
    raffle_id: str,
    username: str,
    display_name: str | None = None,
    twitch_user_id: str | None = None,
    entry_source: EntrySource = EntrySource.chat_command,
    entry_content: str | None = None,
    source_event_id: str | None = None,
):
    raffle_response = supabase.table("raffles").select("*").eq("id", raffle_id).single().execute()
    raffle = raffle_response.data

    if not raffle:
        raise HTTPException(status_code=404, detail="Sorteo no encontrado.")
    if raffle["status"] != "active":
        raise HTTPException(status_code=400, detail="Solo se pueden registrar participantes en sorteos activos.")

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
