from typing import Optional

from pydantic import BaseModel

from app.schemas.enums import EntrySource


class CreateParticipantRequest(BaseModel):
    raffle_id: str
    username: str
    display_name: Optional[str] = None
    twitch_user_id: Optional[str] = None
    entry_source: EntrySource = EntrySource.chat_command
    entry_content: Optional[str] = None
