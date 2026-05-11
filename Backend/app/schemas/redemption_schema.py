from pydantic import BaseModel
from typing import Optional


class SimulateRedemptionRequest(BaseModel):
    raffle_id: str
    username: str
    display_name: Optional[str] = None
    twitch_user_id: Optional[str] = None
    twitch_redemption_id: Optional[str] = None
    reward_id: Optional[str] = None
    reward_title: str = "Recompensa de sorteo"