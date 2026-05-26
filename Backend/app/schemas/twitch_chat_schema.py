from pydantic import BaseModel, Field


class TwitchTestMessageRequest(BaseModel):
    message_id: str = Field(..., min_length=1)
    twitch_user_id: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    display_name: str | None = None
    message_text: str = Field(..., min_length=1)


class TwitchTestMessageResponse(BaseModel):
    message: str
    data: dict
