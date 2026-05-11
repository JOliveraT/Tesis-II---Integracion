from fastapi import APIRouter
from app.services.scoring_service import calculate_participation_score

router = APIRouter(
    prefix="/scoring",
    tags=["Scoring"]
)


@router.post("/calculate/{raffle_id}")
def calculate_scoring(raffle_id: str):
    return calculate_participation_score(raffle_id)