from fastapi import APIRouter

from app.database import supabase
from app.schemas.participant_schema import CreateParticipantRequest
from app.services.participant_service import register_participant_in_raffle

router = APIRouter(prefix="/participants", tags=["Participants"])


@router.get("/")
def get_participants():
    response = supabase.table("participants").select("*").execute()
    return response.data


@router.post("/")
def create_participant(data: CreateParticipantRequest):
    result = register_participant_in_raffle(
        raffle_id=data.raffle_id,
        username=data.username,
        display_name=data.display_name,
        twitch_user_id=data.twitch_user_id,
        entry_source=data.entry_source,
        entry_content=data.entry_content,
    )

    return {
        "message": "Participante registrado correctamente",
        "participant": result["participant"],
        "entry": result["entry"],
    }
