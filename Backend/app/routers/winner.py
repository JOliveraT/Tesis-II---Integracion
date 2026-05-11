from fastapi import APIRouter
from app.services.winner_service import (
    select_weighted_winner,
    start_claim_timer,
    confirm_winner,
    expire_current_claim
)
from app.schemas.winner_schema import StartClaimRequest

router = APIRouter(
    prefix="/winner",
    tags=["Winner"]
)


@router.post("/select/{raffle_id}")
def select_winner(raffle_id: str):
    return select_weighted_winner(raffle_id)


@router.post("/start-claim/{raffle_id}")
def start_claim(raffle_id: str, data: StartClaimRequest):
    return start_claim_timer(
        raffle_id=raffle_id,
        claim_timeout_seconds=data.claim_timeout_seconds
    )


@router.post("/confirm/{raffle_id}")
def confirm_claim(raffle_id: str):
    return confirm_winner(raffle_id)


@router.post("/expire/{raffle_id}")
def expire_claim(raffle_id: str):
    return expire_current_claim(raffle_id)