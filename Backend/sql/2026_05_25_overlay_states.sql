create table if not exists overlay_states (
    id uuid primary key default gen_random_uuid(),
    streamer_id uuid null,
    overlay_token text not null,
    current_state text not null default 'idle',
    payload jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint overlay_states_current_state_check
        check (current_state in ('idle', 'hidden', 'raffle_animation', 'winner_direct'))
);

create unique index if not exists overlay_states_overlay_token_uidx
    on overlay_states (overlay_token);
