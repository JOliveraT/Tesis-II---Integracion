from datetime import datetime
from typing import Any, Dict, Literal

from pydantic import BaseModel, Field

OverlayState = Literal["idle", "hidden", "raffle_animation", "winner_direct", "claim_pending", "claim_confirmed", "claim_expired"]


class OverlayStateResponse(BaseModel):
    overlay_token: str
    current_state: OverlayState
    payload: Dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime | None = None


class OverlayStateUpdateRequest(BaseModel):
    overlay_token: str
    current_state: OverlayState
    payload: Dict[str, Any] = Field(default_factory=dict)


class OverlayHideRequest(BaseModel):
    overlay_token: str


class OverlayMeResponse(BaseModel):
    overlay_token: str
    overlay_url: str


class OverlayRegenerateResponse(BaseModel):
    overlay_token: str
    overlay_url: str
