from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.enums import EntrySource


class CreateParticipantRequest(BaseModel):
    raffle_id: str
    username: str
    display_name: Optional[str] = None
    twitch_user_id: Optional[str] = None
    entry_source: EntrySource = EntrySource.chat_command
    entry_content: Optional[str] = None


class BulkParticipantItem(BaseModel):
    username: str
    display_name: Optional[str] = None
    twitch_user_id: Optional[str] = None
    entry_source: EntrySource = EntrySource.manual


class BulkCreateParticipantsRequest(BaseModel):
    raffle_id: str
    participants: list[BulkParticipantItem] = Field(..., min_length=1, max_length=1000)


class RemoveParticipantRequest(BaseModel):
    reason: Optional[str] = None
