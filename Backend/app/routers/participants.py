from fastapi import APIRouter

from app.database import supabase
from app.schemas.participant_schema import (
    BulkCreateParticipantsRequest,
    CreateParticipantRequest,
)
from app.services.participant_service import (
    bulk_register_participants,
    list_raffle_participants,
    register_participant_in_raffle,
)

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


@router.post("/bulk")
def bulk_create_participants(data: BulkCreateParticipantsRequest):
    return bulk_register_participants(
        raffle_id=data.raffle_id,
        participants=[participant.model_dump() for participant in data.participants],
    )



@router.get("/raffle/{raffle_id}")
def get_raffle_participants(raffle_id: str):
    return list_raffle_participants(raffle_id)
