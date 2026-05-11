from app.config import settings

TWITCH_AUTH_BASE_URL = "https://id.twitch.tv/oauth2"
TWITCH_API_BASE_URL = "https://api.twitch.tv/helix"

TWITCH_CLIENT_ID = settings.twitch_client_id
TWITCH_CLIENT_SECRET = settings.twitch_client_secret
TWITCH_REDIRECT_URI = settings.twitch_redirect_uri

TWITCH_SCOPES = [
    "user:read:email",
    "channel:read:redemptions",
    "chat:read"
]