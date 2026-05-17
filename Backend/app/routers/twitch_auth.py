from typing import Union

from urllib.parse import urlsplit

from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse

from app.schemas.twitch_schema import (
    TwitchAuthURLResponse,
    TwitchConnectedChannelResponse,
    TwitchMeResponse,
)
from app.integrations.twitch.config import TWITCH_REDIRECT_URI
from app.services.twitch_auth_service import disconnect_channel, get_auth_url, get_me, handle_twitch_callback

router = APIRouter(prefix="/twitch", tags=["Twitch Auth"])


@router.get("/auth-url", response_model=TwitchAuthURLResponse)
def twitch_auth_url():
    auth_url = get_auth_url()
    return TwitchAuthURLResponse(auth_url=auth_url)


def _build_profile_redirect(status: str) -> str:
    default_path = "/dashboard-layout/profile"
    if not TWITCH_REDIRECT_URI:
        return f"{default_path}?twitch_oauth={status}"

    parsed = urlsplit(TWITCH_REDIRECT_URI)
    if not parsed.scheme or not parsed.netloc:
        return f"{default_path}?twitch_oauth={status}"

    return f"{parsed.scheme}://{parsed.netloc}{default_path}?twitch_oauth={status}"


@router.get("/callback")
async def twitch_callback(code: str | None = Query(default=None), error: str | None = Query(default=None)):
    if error:
        return RedirectResponse(url=_build_profile_redirect("cancelled"), status_code=302)

    payload = await handle_twitch_callback(code)
    status = "success" if payload.get("connected") else "error"
    return RedirectResponse(url=_build_profile_redirect(status), status_code=302)


@router.get("/me", response_model=Union[TwitchMeResponse, TwitchConnectedChannelResponse])
async def twitch_me(access_token: str | None = Query(default=None)):
    payload = await get_me(access_token=access_token)
    if access_token:
        return TwitchMeResponse(**payload)
    return TwitchConnectedChannelResponse(**payload)


@router.delete("/disconnect", response_model=TwitchConnectedChannelResponse)
async def twitch_disconnect():
    payload = await disconnect_channel()
    return TwitchConnectedChannelResponse(**payload)
