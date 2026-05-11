from pydantic import BaseModel, Field


class StartClaimRequest(BaseModel):
    claim_timeout_seconds: int = Field(
        default=60,
        ge=5,
        le=300
    )