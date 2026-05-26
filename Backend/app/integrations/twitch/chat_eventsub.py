import logging
from collections.abc import Awaitable, Callable

from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope

from app.integrations.twitch.config import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET

logger = logging.getLogger(__name__)


class TwitchChatEventSubClient:
    def __init__(self, *, access_token: str, refresh_token: str | None, scopes: list[str]):
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._scopes = scopes
        self.twitch: Twitch | None = None
        self.eventsub: EventSubWebsocket | None = None
        self.subscription_id: str | None = None

    async def start(
        self,
        *,
        broadcaster_user_id: str,
        user_id: str,
        callback: Callable[[object], Awaitable[None]],
    ) -> str:
        if not TWITCH_CLIENT_ID or not TWITCH_CLIENT_SECRET:
            raise RuntimeError("Faltan credenciales TWITCH_CLIENT_ID o TWITCH_CLIENT_SECRET")

        self.twitch = await Twitch(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)

        auth_scopes = [AuthScope(scope) for scope in self._scopes]
        await self.twitch.set_user_authentication(
            self._access_token,
            auth_scopes,
            self._refresh_token,
        )

        self.eventsub = EventSubWebsocket(self.twitch)
        self.eventsub.start()

        self.subscription_id = await self.eventsub.listen_channel_chat_message(
            broadcaster_user_id=broadcaster_user_id,
            user_id=user_id,
            callback=callback,
        )
        logger.info(
            "EventSub chat subscription started broadcaster_user_id=%s user_id=%s subscription_id=%s",
            broadcaster_user_id,
            user_id,
            self.subscription_id,
        )
        return self.subscription_id

    async def stop(self) -> None:
        if self.eventsub:
            await self.eventsub.stop()
        if self.twitch:
            await self.twitch.close()
