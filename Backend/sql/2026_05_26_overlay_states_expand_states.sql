-- Expande estados permitidos del overlay sin eliminar datos existentes.
alter table if exists overlay_states
    drop constraint if exists overlay_states_current_state_check;

alter table if exists overlay_states
    add constraint overlay_states_current_state_check
        check (
            current_state in (
                'idle',
                'hidden',
                'raffle_animation',
                'winner_direct',
                'claim_pending',
                'claim_confirmed',
                'claim_expired'
            )
        );
