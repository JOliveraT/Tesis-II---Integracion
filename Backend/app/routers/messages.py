from fastapi import APIRouter

from app.database import supabase
from app.schemas.message_schema import CreateMessageRequest
from app.services.message_service import create_message as create_message_service

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("/")
def get_messages():
    response = supabase.table("chat_messages").select("*").execute()
    return response.data


@router.post("/")
def create_message(data: CreateMessageRequest):
    return create_message_service(data)
