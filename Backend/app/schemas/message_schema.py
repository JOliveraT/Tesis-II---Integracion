from pydantic import BaseModel


class CreateMessageRequest(BaseModel):
    raffle_id: str
    participant_username: str
    content: str