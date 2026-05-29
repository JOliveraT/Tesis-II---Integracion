from app.services import participant_service
from app.schemas.enums import EntrySource
from tests.conftest import FakeSupabase, filters_dict, response


def test_upsert_participant_reuses_existing_raffle_participant(monkeypatch):
    state = {'inserts': []}
    monkeypatch.setattr(participant_service, 'supabase', FakeSupabase())

    def fake_safe(query, detail=None):
        table = query.table_name
        filters = filters_dict(query)
        if table == 'raffles':
            return response({'id': 'raffle-1', 'status': 'active', 'command': '!sorteo'})
        if table == 'participation_entries' and query.action == 'select':
            return response([])
        if table == 'participants' and query.action == 'select':
            return response([{'id': 'participant-1', 'username': 'test_front', 'display_name': 'Test Front'}])
        if table == 'raffle_participants' and query.action == 'select':
            assert filters.get(('eq', 'raffle_id')) == 'raffle-1'
            assert filters.get(('eq', 'participant_id')) == 'participant-1'
            return response([{'id': 'rp-existing', 'raffle_id': 'raffle-1', 'participant_id': 'participant-1'}])
        if query.action == 'insert':
            state['inserts'].append((table, query.payload))
            return response([{**query.payload, 'id': f'{table}-inserted'}])
        return response([])

    monkeypatch.setattr(participant_service, '_safe_supabase', fake_safe)

    result = participant_service.upsert_participant(
        raffle_id='raffle-1',
        username='Test Front',
        display_name='Test Front',
        entry_source=EntrySource.manual,
    )

    assert result['duplicate'] is False
    assert result['participant']['id'] == 'participant-1'
    assert not any(table == 'raffle_participants' for table, _payload in state['inserts'])
    assert any(table == 'participation_entries' for table, _payload in state['inserts'])
