from app.services import twitch_chat_service
from tests.conftest import FakeSupabase, filters_dict, response


def install_chat_fakes(monkeypatch, *, message_text='!sorteo', duplicate_message_id=None, existing_link=False):
    state = {'inserts': []}
    monkeypatch.setattr(twitch_chat_service, 'supabase', FakeSupabase())
    monkeypatch.setattr(twitch_chat_service, 'create_audit_log', lambda **kwargs: None)

    def fake_safe(query):
        table = query.table_name
        filters = filters_dict(query)
        if table == 'twitch_channels':
            return response([{'id': 'channel-1', 'user_id': 'streamer-1', 'twitch_user_id': 'tw-streamer'}])
        if table == 'raffles':
            return response([{'id': 'raffle-1', 'command': '!sorteo', 'status': 'active', 'channel_id': 'channel-1'}])
        if table == 'participation_entries' and query.action == 'select':
            source_event_id = filters.get(('eq', 'source_event_id'))
            if source_event_id == duplicate_message_id:
                return response([{'id': 'entry-existing'}])
            return response([])
        if table == 'participants' and query.action == 'select':
            if ('eq', 'twitch_user_id') in filters or ('eq', 'username') in filters:
                return response([{'id': 'participant-1', 'username': 'test_front', 'display_name': 'Test Front', 'twitch_user_id': 'tw-user'}])
        if table == 'raffle_participants' and query.action == 'select':
            return response([{'id': 'rp-existing'}] if existing_link else [])
        if query.action == 'insert':
            state['inserts'].append((table, query.payload))
            return response([{**query.payload, 'id': f'{table}-inserted'}])
        return response([])

    monkeypatch.setattr(twitch_chat_service, '_safe_supabase', fake_safe)
    return state


def call_process_chat(message_id='msg-1', message_text='!sorteo'):
    return twitch_chat_service.process_chat_message(
        streamer_user_id='streamer-1',
        message_id=message_id,
        twitch_user_id='tw-user',
        username='Test Front',
        display_name='Test Front',
        message_text=message_text,
    )


def test_sorteo_command_registers_participation(monkeypatch):
    state = install_chat_fakes(monkeypatch)

    result = call_process_chat(message_text='!sorteo')

    assert result['data']['is_command'] is True
    assert result['data']['participant_registered'] is True
    assert result['data']['entry_created'] is True
    assert any(table == 'raffle_participants' for table, _payload in state['inserts'])
    assert any(table == 'participation_entries' for table, _payload in state['inserts'])


def test_non_command_message_does_not_register_participation(monkeypatch):
    state = install_chat_fakes(monkeypatch)

    result = call_process_chat(message_text='hola')

    assert result['data']['is_command'] is False
    assert result['data']['participant_registered'] is False
    assert result['data']['entry_created'] is False
    assert not any(table == 'raffle_participants' for table, _payload in state['inserts'])
    assert not any(table == 'participation_entries' for table, _payload in state['inserts'])


def test_duplicate_message_id_returns_duplicate_event_without_server_error(monkeypatch):
    install_chat_fakes(monkeypatch, duplicate_message_id='msg-duplicated')

    result = call_process_chat(message_id='msg-duplicated')

    assert result['data']['duplicate_event'] is True
