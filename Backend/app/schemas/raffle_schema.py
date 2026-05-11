from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.enums import ConfirmationMode


class CreateRaffleRequest(BaseModel):
    title: str
    prize_title: str
    prize_description: Optional[str] = None
    command: str = "!sorteo"
    confirmation_mode: ConfirmationMode = ConfirmationMode.instant
    claim_timeout_seconds: int = Field(default=60, ge=0, le=300)
