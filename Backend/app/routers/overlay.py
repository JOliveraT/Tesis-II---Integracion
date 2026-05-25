from fastapi import APIRouter, Depends

from app.config import settings
from app.schemas.overlay_schema import (
    OverlayHideRequest,
    OverlayMeResponse,
    OverlayRegenerateResponse,
    OverlayStateResponse,
    OverlayStateUpdateRequest,
)
from app.services.auth_service import get_current_user
from app.services.overlay_service import (
    get_or_create_user_overlay,
    get_overlay_state,
    hide_overlay,
    regenerate_user_overlay,
    update_overlay_state,
)

router = APIRouter(prefix="/overlay", tags=["Overlay"])


@router.get("/me", response_model=OverlayMeResponse)
def get_my_overlay(user=Depends(get_current_user)):
    return get_or_create_user_overlay(user_id=user["id"], frontend_base_url=settings.frontend_base_url or "http://localhost:3000")


@router.post("/regenerate-token", response_model=OverlayRegenerateResponse)
def regenerate_overlay_token(user=Depends(get_current_user)):
    return regenerate_user_overlay(user_id=user["id"], frontend_base_url=settings.frontend_base_url or "http://localhost:3000")


@router.get("/state/{overlay_token}", response_model=OverlayStateResponse)
def get_state(overlay_token: str):
    return get_overlay_state(overlay_token)


@router.post("/state", response_model=OverlayStateResponse)
def update_state(data: OverlayStateUpdateRequest):
    # TODO: exigir auth del streamer y validar ownership del overlay_token.
    return update_overlay_state(
        overlay_token=data.overlay_token,
        current_state=data.current_state,
        payload=data.payload,
    )


@router.post("/hide", response_model=OverlayStateResponse)
def hide(data: OverlayHideRequest):
    # TODO: exigir auth del streamer y validar ownership del overlay_token.
    return hide_overlay(data.overlay_token)
