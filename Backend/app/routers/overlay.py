from fastapi import APIRouter

from app.schemas.overlay_schema import (
    OverlayHideRequest,
    OverlayStateResponse,
    OverlayStateUpdateRequest,
)
from app.services.overlay_service import get_overlay_state, hide_overlay, update_overlay_state

router = APIRouter(prefix="/overlay", tags=["Overlay"])


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
    return hide_overlay(data.overlay_token)
