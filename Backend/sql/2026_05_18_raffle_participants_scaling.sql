-- Incremental migration for raffle participants scaling and soft-removal support.

ALTER TABLE public.raffles
ADD COLUMN IF NOT EXISTS summary_snapshot jsonb;

ALTER TABLE public.raffle_participants
ADD COLUMN IF NOT EXISTS removed_at timestamp with time zone;

ALTER TABLE public.raffle_participants
ADD COLUMN IF NOT EXISTS removed_by uuid;

ALTER TABLE public.raffle_participants
ADD COLUMN IF NOT EXISTS removal_reason text;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'raffle_participants_removed_by_fkey'
          AND conrelid = 'public.raffle_participants'::regclass
    ) THEN
        ALTER TABLE public.raffle_participants
        ADD CONSTRAINT raffle_participants_removed_by_fkey
        FOREIGN KEY (removed_by)
        REFERENCES public.users(id);
    END IF;
END;
$$;

CREATE INDEX IF NOT EXISTS idx_raffles_channel_id_created_at
    ON public.raffles(channel_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_raffles_status
    ON public.raffles(status);
CREATE INDEX IF NOT EXISTS idx_raffles_created_at
    ON public.raffles(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_raffle_participants_raffle_id
    ON public.raffle_participants(raffle_id);
CREATE INDEX IF NOT EXISTS idx_raffle_participants_raffle_status
    ON public.raffle_participants(raffle_id, status);
CREATE INDEX IF NOT EXISTS idx_raffle_participants_raffle_entry_source
    ON public.raffle_participants(raffle_id, entry_source);
CREATE INDEX IF NOT EXISTS idx_raffle_participants_participant_id
    ON public.raffle_participants(participant_id);

CREATE INDEX IF NOT EXISTS idx_participation_entries_raffle_id
    ON public.participation_entries(raffle_id);
CREATE INDEX IF NOT EXISTS idx_participation_entries_raffle_entry_type
    ON public.participation_entries(raffle_id, entry_type);
CREATE INDEX IF NOT EXISTS idx_participation_entries_source_event_id
    ON public.participation_entries(source_event_id);

CREATE INDEX IF NOT EXISTS idx_participants_username
    ON public.participants(username);
CREATE INDEX IF NOT EXISTS idx_participants_twitch_user_id
    ON public.participants(twitch_user_id);

CREATE UNIQUE INDEX IF NOT EXISTS uq_raffle_participants_raffle_participant
    ON public.raffle_participants(raffle_id, participant_id);

-- NOTE: this unique partial index can fail if duplicated source_event_id already exists.
CREATE UNIQUE INDEX IF NOT EXISTS uq_participation_entries_source_event_id
    ON public.participation_entries(source_event_id)
    WHERE source_event_id IS NOT NULL;
