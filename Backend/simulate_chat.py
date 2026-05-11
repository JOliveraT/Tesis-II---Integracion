from app.integrations.twitch.chat import handle_incoming_chat_message

# UUID del sorteo creado en Supabase
raffle_id = "37ce011e-6bdf-4829-98f4-51c9b277b8eb"

handle_incoming_chat_message(
    raffle_id=raffle_id,
    twitch_channel_id="123456",
    username="viewer_demo",
    message_text="!mi_sorteo",
    display_name="Viewer Demo",
    viewer_twitch_user_id="654321",
    source_event_id="evt-test-001"
)