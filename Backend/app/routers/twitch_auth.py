from typing import Union

from fastapi import APIRouter, HTTPException, Query

from app.schemas.twitch_schema import (
    TwitchAuthURLResponse,
    TwitchCallbackResponse,
    TwitchConnectedChannelResponse,
    TwitchMeResponse,
)
from app.services.twitch_auth_service import get_auth_url, get_me, handle_twitch_callback

router = APIRouter(prefix="/twitch", tags=["Twitch Auth"])


@router.get("/auth-url", response_model=TwitchAuthURLResponse)
def twitch_auth_url():
    auth_url = get_auth_url()
    return TwitchAuthURLResponse(auth_url=auth_url)


@router.get("/callback", response_model=TwitchCallbackResponse)
async def twitch_callback(code: str | None = Query(default=None), error: str | None = Query(default=None)):
    if error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
    return TwitchCallbackResponse(**(await handle_twitch_callback(code)))


@router.get("/me", response_model=Union[TwitchMeResponse, TwitchConnectedChannelResponse])
async def twitch_me(access_token: str | None = Query(default=None)):
    payload = await get_me(access_token=access_token)
    if access_token:
        return TwitchMeResponse(**payload)
    return TwitchConnectedChannelResponse(**payload)
