from fastapi import APIRouter, Header, HTTPException, Request
from app.schemas.redemption_schema import SimulateRedemptionRequest
from app.services.redemption_service import simulate_channel_point_redemption
from app.services.message_service import process_eventsub_participation_event

router = APIRouter(
    prefix="/redemptions",
    tags=["Redemptions"]
)


@router.post("/simulate")
def simulate_redemption(data: SimulateRedemptionRequest):
    return simulate_channel_point_redemption(data)


@router.post("/twitch")
async def twitch_eventsub_redemptions(
    request: Request,
    twitch_eventsub_message_type: str = Header(default="", alias="Twitch-Eventsub-Message-Type"),
    twitch_eventsub_subscription_type: str = Header(default="", alias="Twitch-Eventsub-Subscription-Type"),
):
    payload = await request.json()

    if twitch_eventsub_message_type == "webhook_callback_verification":
        challenge = payload.get("challenge")
        if not challenge:
            raise HTTPException(status_code=400, detail="Missing EventSub challenge")
        return {"challenge": challenge}

    if twitch_eventsub_message_type == "notification":
        event_data = payload.get("event", {})
        result = process_eventsub_participation_event(
            event_type=twitch_eventsub_subscription_type or "unknown",
            event_payload=event_data,
        )
        return {"ok": True, "result": result}

    if twitch_eventsub_message_type == "revocation":
        return {"ok": True, "revoked": True, "payload": payload}

    return {"ok": True, "ignored": True}
