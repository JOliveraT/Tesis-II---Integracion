from app.services import scoring_service
from tests.conftest import FakeSupabase, filters_dict, response


def test_valid_participant_receives_non_negative_score_and_is_eligible(monkeypatch):
    monkeypatch.setattr(scoring_service, 'supabase', FakeSupabase())

    def fake_safe(query):
        table = query.table_name
        filters = filters_dict(query)
        if table == 'raffles':
            return response({'id': 'raffle-1', 'status': 'active'})
        if table == 'raffle_participants' and query.action == 'select':
            return response([{'participant_id': 'participant-1'}])
        if table == 'participants':
            return response({'id': 'participant-1', 'username': 'test_front'})
        if table == 'chat_messages':
            assert filters.get(('eq', 'participant_id')) == 'participant-1'
            return response([
                {'message_text': '!sorteo', 'is_command': True},
                {'message_text': 'hola chat', 'is_command': False},
            ])
        if table == 'channel_point_redemptions':
            return response([])
        if table == 'participation_scores' and query.action == 'insert':
            return response([{**query.payload, 'id': 'score-1'}])
        if query.action in {'delete', 'update'}:
            return response([])
        return response([])

    monkeypatch.setattr(scoring_service, '_safe_supabase', fake_safe)

    result = scoring_service.calculate_participation_score('raffle-1')

    score = result['results'][0]
    assert score['final_score'] >= 0
    assert score['eligible'] is True
