"""Twitch EventSub integration helpers."""

from __future__ import annotations

import logging
from functools import lru_cache

from twitchAPI.eventsub.webhook import EventSubWebhook
from twitchAPI.twitch import Twitch

from app.config import settings
from app.database import supabase
from app.services.message_service import process_chat_command_participation


logger = logging.getLogger(__name__)


@lru_cache
def get_twitch_client() -> Twitch:
    """Create and cache a Twitch client using env configuration."""
    if not settings.twitch_client_id or not settings.twitch_client_secret:
        raise ValueError("TWITCH_CLIENT_ID and TWITCH_CLIENT_SECRET are required")
    return Twitch(settings.twitch_client_id, settings.twitch_client_secret)


def subscribe_eventsub_for_connected_channels(
    callback_url: str,
    webhook_secret: str,
    enable_subscribe_events: bool = False,
) -> EventSubWebhook:
    """Subscribe EventSub webhook topics for all connected twitch channels."""
    twitch = get_twitch_client()
    eventsub = EventSubWebhook(callback_url, 8080, twitch, webhook_secret)

    channels = (
        supabase.table("twitch_channels")
        .select("twitch_user_id")
        .not_.is_("twitch_user_id", "null")
        .execute()
    )

    for channel in channels.data or []:
        broadcaster_id = channel.get("twitch_user_id")
        if not broadcaster_id:
            continue

        eventsub.listen_channel_points_custom_reward_redemption_add(
            broadcaster_id,
            handle_channel_point_redemption,
        )
        if enable_subscribe_events:
            eventsub.listen_channel_subscribe(broadcaster_id, handle_channel_subscription)

        logger.info("EventSub subscriptions requested for channel %s", broadcaster_id)

    return eventsub


def handle_channel_point_redemption(payload: dict) -> dict:
    """Transform EventSub redemption payload and process raffle command participation."""
    event = payload.get("event", payload)
    broadcaster_user_id = event.get("broadcaster_user_id")
    viewer_username = event.get("user_login") or event.get("user_name") or ""
    reward_title = ((event.get("reward") or {}).get("title")) or ""
    user_input = event.get("user_input") or ""
    raffle_id = event.get("reward_id") or ((event.get("reward") or {}).get("id")) or ""
    source_event_id = event.get("id") or f"redemption:{broadcaster_user_id}:{viewer_username}:{reward_title}:{user_input}"

    return process_chat_command_participation(
        raffle_id=raffle_id,
        twitch_channel_id=broadcaster_user_id,
        username=viewer_username,
        message_text=user_input or reward_title,
        display_name=event.get("user_name"),
        twitch_user_id=event.get("user_id"),
        source_event_id=source_event_id,
    )


def handle_channel_subscription(payload: dict) -> dict:
    """Placeholder to support future subscription-based entries."""
    return {"received": True, "type": "channel.subscribe", "payload": payload}


def handle_incoming_chat_message(
    *,
    raffle_id: str,
    twitch_channel_id: str,
    username: str,
    message_text: str,
    display_name: str | None = None,
    viewer_twitch_user_id: str | None = None,
    source_event_id: str | None = None,
) -> dict:
    """Validate channel command and register participant when the command matches."""
    return process_chat_command_participation(
        raffle_id=raffle_id,
        twitch_channel_id=twitch_channel_id,
        username=username,
        message_text=message_text,
        display_name=display_name,
        twitch_user_id=viewer_twitch_user_id,
        source_event_id=source_event_id,
    )
