from pydantic import BaseModel, Field


class TwitchAuthURLResponse(BaseModel):
    auth_url: str


class TwitchChannelData(BaseModel):
    twitch_user_id: str
    login: str
    display_name: str
    email: str | None = None
    profile_image_url: str | None = None


class TwitchConnectedChannelResponse(BaseModel):
    connected: bool
    message: str
    channel: TwitchChannelData | None = None


class TwitchCallbackResponse(TwitchConnectedChannelResponse):
    token_saved: bool = Field(default=False)


class TwitchMeResponse(BaseModel):
    data: list[dict] = Field(default_factory=list)


class TwitchEventSubReward(BaseModel):
    id: str | None = None
    title: str | None = None


class TwitchEventSubEvent(BaseModel):
    id: str | None = None
    broadcaster_user_id: str
    user_id: str | None = None
    user_login: str | None = None
    user_name: str | None = None
    user_input: str | None = None
    message: dict | None = None
    reward: TwitchEventSubReward | None = None


class TwitchEventSubEnvelope(BaseModel):
    challenge: str | None = None
    event: TwitchEventSubEvent | None = None
