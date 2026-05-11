from fastapi import HTTPException
from app.database import supabase


def get_raffle_summary(raffle_id: str):
    # 1. Datos del sorteo
    raffle_response = supabase.table("raffles") \
        .select("*") \
        .eq("id", raffle_id) \
        .single() \
        .execute()

    raffle = raffle_response.data

    if not raffle:
        raise HTTPException(
            status_code=404,
            detail="Sorteo no encontrado."
        )

    # 2. Participantes asociados al sorteo
    raffle_participants_response = supabase.table("raffle_participants") \
        .select("*") \
        .eq("raffle_id", raffle_id) \
        .execute()

    raffle_participants = raffle_participants_response.data

    participants_detail = []

    for rp in raffle_participants:
        participant_response = supabase.table("participants") \
            .select("*") \
            .eq("id", rp["participant_id"]) \
            .single() \
            .execute()

        participant = participant_response.data

        if participant:
            participants_detail.append({
                "raffle_participant_id": rp["id"],
                "participant_id": participant["id"],
                "username": participant["username"],
                "display_name": participant["display_name"],
                "entry_source": rp["entry_source"],
                "status": rp["status"],
                "is_eligible": rp["is_eligible"],
                "final_score": rp["final_score"],
                "joined_at": rp["joined_at"]
            })

    # 3. Mensajes del sorteo
    messages_response = supabase.table("chat_messages") \
        .select("*") \
        .eq("raffle_id", raffle_id) \
        .order("sent_at", desc=False) \
        .execute()

    messages = messages_response.data

    # 4. Entradas de participación
    entries_response = supabase.table("participation_entries") \
        .select("*") \
        .eq("raffle_id", raffle_id) \
        .order("created_at", desc=False) \
        .execute()

    participation_entries = entries_response.data

    # 5. Scores calculados
    scores_response = supabase.table("participation_scores") \
        .select("*") \
        .eq("raffle_id", raffle_id) \
        .order("final_score", desc=True) \
        .execute()

    scores = scores_response.data

    # 6. Resultado o candidato ganador
    results_response = supabase.table("raffle_results") \
        .select("*") \
        .eq("raffle_id", raffle_id) \
        .order("selected_at", desc=True) \
        .execute()

    results = results_response.data

    current_result = results[0] if results else None

    # 7. Auditoría
    audit_response = supabase.table("audit_logs") \
        .select("*") \
        .eq("raffle_id", raffle_id) \
        .order("created_at", desc=True) \
        .execute()

    audit_logs = audit_response.data

    return {
        "raffle": raffle,
        "participants_count": len(participants_detail),
        "messages_count": len(messages),
        "scores_count": len(scores),
        "participants": participants_detail,
        "messages": messages,
        "participation_entries": participation_entries,
        "scores": scores,
        "current_result": current_result,
        "results_history": results,
        "audit_logs": audit_logs
    }