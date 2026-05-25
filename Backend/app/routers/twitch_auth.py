from typing import Union
import logging

from urllib.parse import urlencode, urljoin

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse

from app.schemas.twitch_schema import (
    TwitchAuthURLResponse,
    TwitchConnectedChannelResponse,
    TwitchMeResponse,
)
from app.integrations.twitch.config import FRONTEND_BASE_URL
from app.services.auth_service import get_current_user
from app.services.twitch_auth_service import disconnect_channel, get_auth_url, get_me, handle_twitch_callback

router = APIRouter(prefix="/twitch", tags=["Twitch Auth"])
logger = logging.getLogger(__name__)


@router.get("/auth-url", response_model=TwitchAuthURLResponse)
def twitch_auth_url(user=Depends(get_current_user)):
    auth_url = get_auth_url(user_id=user["id"])
    return TwitchAuthURLResponse(auth_url=auth_url)


def _build_profile_redirect(status: str) -> str:
    base_url = (FRONTEND_BASE_URL or "http://localhost:3000").rstrip("/")
    profile_url = urljoin(f"{base_url}/", "dashboard-layout/profile")
    query = urlencode({"twitch_oauth": status})
    return f"{profile_url}?{query}"


@router.get("/callback")
async def twitch_callback(code: str | None = Query(default=None), state: str | None = Query(default=None), error: str | None = Query(default=None)):
    if error:
        return RedirectResponse(url=_build_profile_redirect("cancelled"), status_code=302)

    try:
        payload = await handle_twitch_callback(code, state)
        status = "success" if payload.get("connected") else "error"
    except HTTPException as exc:
        logger.error("/twitch/callback controlled error detail=%s", exc.detail)
        status = "error"
    except Exception:
        logger.exception("/twitch/callback unexpected error")
        status = "error"

    return RedirectResponse(url=_build_profile_redirect(status), status_code=302)


@router.get("/me", response_model=Union[TwitchMeResponse, TwitchConnectedChannelResponse])
async def twitch_me(access_token: str | None = Query(default=None), user=Depends(get_current_user)):
    payload = await get_me(user_id=user["id"], access_token=access_token)
    if access_token:
        return TwitchMeResponse(**payload)
    return TwitchConnectedChannelResponse(**payload)


@router.delete("/disconnect", response_model=TwitchConnectedChannelResponse)
async def twitch_disconnect(user=Depends(get_current_user)):
    payload = await disconnect_channel(user_id=user["id"])
    return TwitchConnectedChannelResponse(**payload)
