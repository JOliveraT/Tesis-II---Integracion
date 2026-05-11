from fastapi import HTTPException

from app.database import supabase
from app.schemas.enums import EntrySource
from app.services.audit_service import create_audit_log
from app.services.participant_service import register_participant_in_raffle


def simulate_channel_point_redemption(data):
    if data.twitch_redemption_id:
        duplicated = supabase.table("channel_point_redemptions").select("*").eq("twitch_redemption_id", data.twitch_redemption_id).execute()
        if duplicated.data:
            raise HTTPException(status_code=409, detail="Este twitch_redemption_id ya fue procesado.")

    entry_content = f"Canjeó recompensa del canal: {data.reward_title}"
    result = register_participant_in_raffle(
        raffle_id=data.raffle_id,
        username=data.username,
        display_name=data.display_name,
        twitch_user_id=data.twitch_user_id,
        entry_source=EntrySource.channel_points_reward,
        entry_content=entry_content,
        source_event_id=data.twitch_redemption_id,
    )

    if result.get("duplicate"):
        raise HTTPException(status_code=409, detail="Este source_event_id ya fue procesado para el sorteo.")

    participant = result["participant"]
    redemption_response = supabase.table("channel_point_redemptions").insert(
        {
            "raffle_id": data.raffle_id,
            "participant_id": participant["id"],
            "twitch_redemption_id": data.twitch_redemption_id,
            "reward_id": data.reward_id,
            "reward_title": data.reward_title,
            "status": "redeemed",
        }
    ).execute()

    create_audit_log(
        raffle_id=data.raffle_id,
        participant_id=participant["id"],
        action="channel_points_redemption_simulated",
        detail=f"Participante ingresó al sorteo mediante canje de recompensa: {data.reward_title}.",
    )

    return {
        "message": "Canje de puntos simulado correctamente.",
        "participant": participant,
        "participation_entry": result["entry"],
        "redemption": redemption_response.data,
    }
