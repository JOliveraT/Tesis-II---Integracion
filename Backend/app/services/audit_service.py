from app.database import supabase


def create_audit_log(
    raffle_id: str,
    action: str,
    detail: str,
    participant_id: str | None = None,
):
    response = supabase.table("audit_logs").insert(
        {
            "raffle_id": raffle_id,
            "participant_id": participant_id,
            "action": action,
            "detail": detail,
        }
    ).execute()

    return response.data[0] if response.data else None
