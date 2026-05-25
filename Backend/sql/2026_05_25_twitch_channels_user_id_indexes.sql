CREATE INDEX IF NOT EXISTS idx_twitch_channels_user_id
ON public.twitch_channels(user_id);

CREATE UNIQUE INDEX IF NOT EXISTS idx_twitch_channels_user_id_unique
ON public.twitch_channels(user_id)
WHERE user_id IS NOT NULL;
