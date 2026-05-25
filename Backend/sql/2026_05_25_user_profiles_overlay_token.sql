ALTER TABLE public.user_profiles
ADD COLUMN IF NOT EXISTS overlay_token text;

CREATE UNIQUE INDEX IF NOT EXISTS idx_user_profiles_overlay_token
ON public.user_profiles(overlay_token)
WHERE overlay_token IS NOT NULL;
