import httpx
from fastapi import HTTPException

from app.database import supabase
from app.services.supabase_retry import RETRYABLE_SUPABASE_ERRORS, execute_with_retry


RETRYABLE_ERRORS = RETRYABLE_SUPABASE_ERRORS


def _safe_supabase(query):
    try:
        return execute_with_retry(query)
    except RETRYABLE_ERRORS as error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo calcular temporalmente el puntaje. Inténtalo nuevamente.",
        ) from error


def calculate_participation_score(raffle_id: str):
    raffle_response = _safe_supabase(
        supabase.table("raffles").select("*").eq("id", raffle_id).single()
    )

    raffle = raffle_response.data

    if not raffle:
        raise HTTPException(status_code=404, detail="Sorteo no encontrado.")

    if raffle["status"] != "active":
        raise HTTPException(
            status_code=400,
            detail="Solo se puede calcular participación en sorteos activos.",
        )

    _safe_supabase(
        supabase.table("participation_scores").delete().eq("raffle_id", raffle_id)
    )

    raffle_participants_response = _safe_supabase(
        supabase.table("raffle_participants")
        .select("participant_id")
        .eq("raffle_id", raffle_id)
        .neq("status", "removed")
    )

    results = []

    for rp in raffle_participants_response.data:
        participant_id = rp["participant_id"]

        participant_response = _safe_supabase(
            supabase.table("participants").select("*").eq("id", participant_id).single()
        )

        participant = participant_response.data

        messages_response = _safe_supabase(
            supabase.table("chat_messages")
            .select("*")
            .eq("raffle_id", raffle_id)
            .eq("participant_id", participant_id)
        )

        user_messages = messages_response.data

        total_messages = len(user_messages)
        unique_messages = len(set(m["message_text"].lower().strip() for m in user_messages))

        repeated_penalty = max(0, total_messages - unique_messages) * 5
        command_used = any(m["is_command"] is True for m in user_messages)

        reward_response = _safe_supabase(
            supabase.table("channel_point_redemptions")
            .select("*")
            .eq("raffle_id", raffle_id)
            .eq("participant_id", participant_id)
        )

        reward_used = len(reward_response.data) > 0

        frequency_score = min(total_messages * 10, 40)
        diversity_score = min(unique_messages * 10, 30)
        engagement_score = 20 if command_used else 0

        if reward_used:
            engagement_score += 10

        text_quality_score = 10

        final_score = frequency_score + diversity_score + engagement_score + text_quality_score - repeated_penalty

        final_score = max(0, min(final_score, 100))
        is_eligible = final_score >= 0

        reason = (
            "Participación válida con interacción suficiente."
            if is_eligible
            else "Participación insuficiente o con señales de repetición."
        )

        score_response = _safe_supabase(
            supabase.table("participation_scores")
            .insert(
                {
                    "raffle_id": raffle_id,
                    "participant_id": participant_id,
                    "message_count": total_messages,
                    "unique_message_count": unique_messages,
                    "command_used": command_used,
                    "reward_used": reward_used,
                    "frequency_score": frequency_score,
                    "diversity_score": diversity_score,
                    "engagement_score": engagement_score,
                    "behavior_penalty": repeated_penalty,
                    "text_quality_score": text_quality_score,
                    "final_score": final_score,
                    "is_eligible": is_eligible,
                    "reason": reason,
                }
            )
        )

        _safe_supabase(
            supabase.table("raffle_participants")
            .update({"is_eligible": is_eligible, "final_score": final_score, "status": "evaluated"})
            .eq("raffle_id", raffle_id)
            .eq("participant_id", participant_id)
        )

        results.append(
            {
                "username": participant["username"],
                "total_messages": total_messages,
                "unique_messages": unique_messages,
                "command_used": command_used,
                "reward_used": reward_used,
                "final_score": final_score,
                "eligible": is_eligible,
                "reason": reason,
                "saved_score": score_response.data,
            }
        )

    return {"raffle_id": raffle_id, "participants_evaluated": len(results), "results": results}
