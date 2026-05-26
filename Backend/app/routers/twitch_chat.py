from fastapi import APIRouter, Depends

from app.schemas.twitch_chat_schema import TwitchTestMessageRequest
from app.services.auth_service import get_current_user
from app.services.twitch_chat_service import process_test_message

router = APIRouter(prefix="/twitch/chat", tags=["Twitch Chat"])


@router.post("/test-message")
def process_twitch_test_message(data: TwitchTestMessageRequest, user=Depends(get_current_user)):
    return process_test_message(
        user_id=user["id"],
        message_id=data.message_id,
        twitch_user_id=data.twitch_user_id,
        username=data.username,
        display_name=data.display_name,
        message_text=data.message_text,
    )
