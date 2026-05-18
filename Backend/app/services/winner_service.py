import random
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from app.database import supabase


def get_current_pending_result(raffle_id: str):
    response = supabase.table("raffle_results") \
        .select("*") \
        .eq("raffle_id", raffle_id) \
        .in_("claim_status", ["waiting_start", "pending"]) \
        .execute()

    if response.data:
        return response.data[0]

    return None


def select_weighted_winner(raffle_id: str):
    raffle_response = supabase.table("raffles") \
        .select("*") \
        .eq("id", raffle_id) \
        .single() \
        .execute()

    raffle = raffle_response.data

    if not raffle:
        raise HTTPException(status_code=404, detail="Sorteo no encontrado.")

    if raffle["status"] != "active":
        raise HTTPException(
            status_code=400,
            detail="Solo se puede seleccionar ganador en sorteos activos."
        )

    existing_confirmed = supabase.table("raffle_results") \
        .select("*") \
        .eq("raffle_id", raffle_id) \
        .eq("claim_status", "confirmed") \
        .execute()

    if existing_confirmed.data:
        raise HTTPException(
            status_code=400,
            detail="Este sorteo ya tiene un ganador confirmado."
        )

    current_pending = get_current_pending_result(raffle_id)

    if current_pending:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un candidato ganador pendiente de confirmación."
        )

    expired_results = supabase.table("raffle_results") \
        .select("winner_participant_id") \
        .eq("raffle_id", raffle_id) \
        .eq("claim_status", "expired") \
        .execute()

    expired_participant_ids = {
        item["winner_participant_id"]
        for item in expired_results.data
        if item.get("winner_participant_id")
    }

    participants_response = supabase.table("raffle_participants") \
        .select("participant_id, final_score, is_eligible") \
        .eq("raffle_id", raffle_id) \
        .eq("is_eligible", True) \
        .neq("status", "removed") \
        .execute()

    eligible_participants = participants_response.data

    if not eligible_participants:
        raise HTTPException(
            status_code=400,
            detail="No hay participantes elegibles para seleccionar ganador."
        )

    weighted_pool = []

    for participant in eligible_participants:
        participant_id = participant["participant_id"]

        if participant_id in expired_participant_ids:
            continue

        score = float(participant["final_score"] or 0)

        if score > 0:
            weighted_pool.append({
                "participant_id": participant_id,
                "weight": score
            })

    if not weighted_pool:
        raise HTTPException(
            status_code=400,
            detail="No hay participantes disponibles con puntaje válido."
        )

    selected = random.choices(
        population=weighted_pool,
        weights=[item["weight"] for item in weighted_pool],
        k=1
    )[0]

    participant_response = supabase.table("participants") \
        .select("*") \
        .eq("id", selected["participant_id"]) \
        .single() \
        .execute()

    winner = participant_response.data

    confirmation_mode = raffle.get("confirmation_mode", "instant")

    if confirmation_mode == "instant":
        claim_status = "confirmed"
        raffle_status = "finished"
        confirmed_at = datetime.now(timezone.utc).isoformat()
        claim_timeout_seconds = 0
        claim_started_at = None
        claim_expires_at = None
    else:
        claim_status = "waiting_start"
        raffle_status = "pending_claim"
        confirmed_at = None
        claim_timeout_seconds = None
        claim_started_at = None
        claim_expires_at = None

    result_response = supabase.table("raffle_results") \
        .insert({
            "raffle_id": raffle_id,
            "winner_participant_id": winner["id"],
            "winner_username": winner["username"],
            "winner_score": selected["weight"],
            "claim_status": claim_status,
            "claim_timeout_seconds": claim_timeout_seconds,
            "claim_started_at": claim_started_at,
            "claim_expires_at": claim_expires_at,
            "confirmed_at": confirmed_at
        }) \
        .execute()

    supabase.table("raffles") \
        .update({
            "status": raffle_status
        }) \
        .eq("id", raffle_id) \
        .execute()

    supabase.table("audit_logs") \
        .insert({
            "raffle_id": raffle_id,
            "participant_id": winner["id"],
            "action": "winner_selected",
            "detail": f"Candidato ganador seleccionado mediante sorteo ponderado con score {selected['weight']}."
        }) \
        .execute()

    return {
        "message": "Ganador seleccionado correctamente.",
        "raffle_id": raffle_id,
        "winner": {
            "participant_id": winner["id"],
            "username": winner["username"],
            "display_name": winner["display_name"],
            "score": selected["weight"]
        },
        "confirmation_mode": confirmation_mode,
        "claim_status": claim_status,
        "selection_method": "weighted_random",
        "result": result_response.data
    }


def start_claim_timer(raffle_id: str, claim_timeout_seconds: int):
    raffle_response = supabase.table("raffles") \
        .select("*") \
        .eq("id", raffle_id) \
        .single() \
        .execute()

    raffle = raffle_response.data

    if not raffle:
        raise HTTPException(status_code=404, detail="Sorteo no encontrado.")

    if raffle["status"] != "pending_claim":
        raise HTTPException(
            status_code=400,
            detail="El sorteo no está esperando inicio de confirmación."
        )

    result = get_current_pending_result(raffle_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No existe candidato pendiente de confirmación."
        )

    if result["claim_status"] != "waiting_start":
        raise HTTPException(
            status_code=400,
            detail="La confirmación ya fue iniciada o no está disponible."
        )

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=claim_timeout_seconds)

    response = supabase.table("raffle_results") \
        .update({
            "claim_status": "pending",
            "claim_timeout_seconds": claim_timeout_seconds,
            "claim_started_at": now.isoformat(),
            "claim_expires_at": expires_at.isoformat()
        }) \
        .eq("id", result["id"]) \
        .execute()

    supabase.table("audit_logs") \
        .insert({
            "raffle_id": raffle_id,
            "participant_id": result["winner_participant_id"],
            "action": "claim_timer_started",
            "detail": f"Se inició el tiempo de confirmación por {claim_timeout_seconds} segundos."
        }) \
        .execute()

    return {
        "message": "Tiempo de confirmación iniciado.",
        "raffle_id": raffle_id,
        "claim_timeout_seconds": claim_timeout_seconds,
        "claim_started_at": now.isoformat(),
        "claim_expires_at": expires_at.isoformat(),
        "result": response.data
    }


def confirm_winner(raffle_id: str):
    result = get_current_pending_result(raffle_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No hay ganador pendiente de confirmación."
        )

    if result["claim_status"] != "pending":
        raise HTTPException(
            status_code=400,
            detail="El tiempo de confirmación aún no ha iniciado."
        )

    now = datetime.now(timezone.utc)

    if result["claim_expires_at"]:
        expires_at = datetime.fromisoformat(
            result["claim_expires_at"].replace("Z", "+00:00")
        )

        if now > expires_at:
            raise HTTPException(
                status_code=400,
                detail="El tiempo de confirmación ya expiró."
            )

    response = supabase.table("raffle_results") \
        .update({
            "claim_status": "confirmed",
            "confirmed_at": now.isoformat()
        }) \
        .eq("id", result["id"]) \
        .execute()

    supabase.table("raffles") \
        .update({
            "status": "finished"
        }) \
        .eq("id", raffle_id) \
        .execute()

    supabase.table("audit_logs") \
        .insert({
            "raffle_id": raffle_id,
            "participant_id": result["winner_participant_id"],
            "action": "winner_confirmed",
            "detail": "El ganador confirmó su presencia dentro del tiempo establecido."
        }) \
        .execute()

    return {
        "message": "Ganador confirmado correctamente.",
        "raffle_id": raffle_id,
        "result": response.data
    }


def expire_current_claim(raffle_id: str):
    result = get_current_pending_result(raffle_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No hay confirmación pendiente para expirar."
        )

    response = supabase.table("raffle_results") \
        .update({
            "claim_status": "expired"
        }) \
        .eq("id", result["id"]) \
        .execute()

    supabase.table("raffles") \
        .update({
            "status": "active"
        }) \
        .eq("id", raffle_id) \
        .execute()

    supabase.table("audit_logs") \
        .insert({
            "raffle_id": raffle_id,
            "participant_id": result["winner_participant_id"],
            "action": "claim_expired",
            "detail": "El candidato ganador no confirmó dentro del tiempo establecido. El sorteo vuelve a estar activo."
        }) \
        .execute()

    return {
        "message": "Confirmación expirada. El sorteo vuelve a estar activo.",
        "raffle_id": raffle_id,
        "result": response.data
    }