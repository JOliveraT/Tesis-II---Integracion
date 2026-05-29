from app.database import supabase
from app.services.supabase_retry import execute_with_retry


def create_audit_log(
    raffle_id: str,
    action: str,
    detail: str,
    participant_id: str | None = None,
):
    response = execute_with_retry(
        supabase.table("audit_logs").insert(
            {
                "raffle_id": raffle_id,
                "participant_id": participant_id,
                "action": action,
                "detail": detail,
            }
        )
    )

    return response.data[0] if response.data else None
