from fastapi import APIRouter
from app.database import supabase
from app.schemas.participant_schema import RemoveParticipantRequest
from app.schemas.raffle_schema import CreateRaffleRequest
from app.services.participant_service import remove_participant_from_raffle
from app.services.raffle_service import get_raffle_summary

router = APIRouter(
    prefix="/raffles",
    tags=["Raffles"]
)


@router.get("/")
def get_raffles():
    response = supabase.table("raffles").select("*").execute()
    return response.data


@router.get("/{raffle_id}/summary")
def raffle_summary(raffle_id: str):
    return get_raffle_summary(raffle_id)


@router.post("/")
def create_raffle(data: CreateRaffleRequest):
    response = supabase.table("raffles").insert({
        "title": data.title,
        "prize_title": data.prize_title,
        "prize_description": data.prize_description,
        "command": data.command,
        "status": "active",
        "entry_mode": "mixed",
        "volume_mode": "normal",
        "confirmation_mode": data.confirmation_mode,
        "claim_timeout_seconds": data.claim_timeout_seconds
    }).execute()

    return {
        "message": "Sorteo creado correctamente",
        "data": response.data
    }


@router.patch("/{raffle_id}/participants/{participant_id}/remove")
def remove_participant_from_raffle_endpoint(raffle_id: str, participant_id: str, data: RemoveParticipantRequest):
    return remove_participant_from_raffle(raffle_id=raffle_id, participant_id=participant_id, reason=data.reason)
