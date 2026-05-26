import logging
from dataclasses import dataclass

from fastapi import HTTPException

from app.database import supabase
from app.integrations.twitch.chat_eventsub import TwitchChatEventSubClient
from app.services.twitch_chat_service import process_chat_message

logger = logging.getLogger(__name__)

CHAT_EVENT_NAME = "channel.chat.message"
REQUIRED_SCOPE = "user:read:chat"
active_chat_listeners: dict[str, "ActiveChatListener"] = {}


@dataclass
class ActiveChatListener:
    user_id: str
    twitch_user_id: str
    login: str
    event: str
    client: TwitchChatEventSubClient


def _get_user_twitch_channel(user_id: str) -> dict:
    response = (
        supabase.table("twitch_channels")
        .select("user_id,twitch_user_id,login,access_token,refresh_token,scopes")
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .limit(1)
        .execute()
    )
    data = response.data or []
    if not data:
        raise HTTPException(status_code=400, detail="No hay canal de Twitch vinculado.")
    return data[0]


async def start_chat_listener(*, user_id: str) -> dict:
    if user_id in active_chat_listeners:
        active = active_chat_listeners[user_id]
        return {
            "message": "Listener de chat ya estaba activo",
            "data": {
                "active": True,
                "user_id": active.user_id,
                "twitch_user_id": active.twitch_user_id,
                "login": active.login,
                "event": active.event,
            },
        }

    channel = _get_user_twitch_channel(user_id)
    twitch_user_id = (channel.get("twitch_user_id") or "").strip()
    access_token = (channel.get("access_token") or "").strip()
    refresh_token = channel.get("refresh_token")
    scopes = channel.get("scopes") or []
    login = channel.get("login") or ""

    if not twitch_user_id or not access_token:
        raise HTTPException(status_code=400, detail="Canal de Twitch incompleto para iniciar listener.")
    if REQUIRED_SCOPE not in scopes:
        raise HTTPException(status_code=400, detail="Falta el permiso user:read:chat. Vuelve a vincular Twitch.")

    async def _on_chat_message(event: object) -> None:
        try:
            payload = getattr(event, "event", event)
            message_id = str(getattr(payload, "message_id", "") or "").strip()
            chatter_user_id = str(getattr(payload, "chatter_user_id", "") or "").strip()
            chatter_login = str(getattr(payload, "chatter_user_login", "") or "").strip()
            chatter_name = getattr(payload, "chatter_user_name", None)
            message_obj = getattr(payload, "message", None)
            message_text = getattr(message_obj, "text", None) if message_obj else getattr(payload, "message_text", "")
            message_text = str(message_text or "").strip()

            if not message_id or not chatter_user_id or not chatter_login or not message_text:
                logger.warning("EventSub chat event malformed user_id=%s message_id=%s", user_id, message_id)
                return

            result = process_chat_message(
                streamer_user_id=user_id,
                message_id=message_id,
                twitch_user_id=chatter_user_id,
                username=chatter_login,
                display_name=chatter_name,
                message_text=message_text,
            )
            data = result.get("data", {})
            logger.info(
                "EventSub chat processed message_id=%s chatter=%s is_command=%s participant_registered=%s duplicate_event=%s",
                message_id,
                chatter_login,
                data.get("is_command"),
                data.get("participant_registered"),
                data.get("duplicate_event"),
            )
        except Exception as exc:
            logger.warning("Error procesando evento de chat user_id=%s error=%s", user_id, exc)

    client = TwitchChatEventSubClient(
        access_token=access_token,
        refresh_token=refresh_token,
        scopes=scopes,
    )

    try:
        await client.start(
            broadcaster_user_id=twitch_user_id,
            user_id=twitch_user_id,
            callback=_on_chat_message,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("No se pudo iniciar EventSub chat user_id=%s error=%s", user_id, exc)
        raise HTTPException(status_code=500, detail="No se pudo iniciar el listener de chat de Twitch.") from exc

    active_chat_listeners[user_id] = ActiveChatListener(
        user_id=user_id,
        twitch_user_id=twitch_user_id,
        login=login,
        event=CHAT_EVENT_NAME,
        client=client,
    )
    return {
        "message": "Listener de chat iniciado",
        "data": {
            "active": True,
            "user_id": user_id,
            "twitch_user_id": twitch_user_id,
            "login": login,
            "event": CHAT_EVENT_NAME,
        },
    }


async def stop_chat_listener(*, user_id: str) -> dict:
    active = active_chat_listeners.get(user_id)
    if not active:
        return {"message": "Listener de chat no estaba activo", "data": {"active": False, "event": CHAT_EVENT_NAME}}
    try:
        await active.client.stop()
    except Exception as exc:
        logger.warning("Error deteniendo listener user_id=%s error=%s", user_id, exc)
    active_chat_listeners.pop(user_id, None)
    return {"message": "Listener de chat detenido", "data": {"active": False, "event": CHAT_EVENT_NAME}}


def get_chat_listener_status(*, user_id: str) -> dict:
    active = active_chat_listeners.get(user_id)
    return {
        "message": "Estado del listener de chat",
        "data": {
            "active": bool(active),
            "event": CHAT_EVENT_NAME,
        },
    }
