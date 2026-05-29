import pytest
from fastapi import HTTPException

from app.services import winner_service
from tests.conftest import FakeSupabase, response


def install_winner_fakes(monkeypatch, eligible_participants):
    monkeypatch.setattr(winner_service, 'supabase', FakeSupabase())
    monkeypatch.setattr(winner_service.random, 'choices', lambda population, weights, k: [population[0]])

    def fake_safe(query):
        table = query.table_name
        if table == 'raffles' and query.action == 'select':
            return response({'id': 'raffle-1', 'status': 'active', 'confirmation_mode': 'instant'})
        if table == 'raffle_results' and query.action == 'select':
            selected = query.selected or '*'
            if selected == 'winner_participant_id':
                return response([])
            return response([])
        if table == 'raffle_participants':
            return response(eligible_participants)
        if table == 'participants':
            return response({'id': 'participant-1', 'username': 'test_front', 'display_name': 'Test Front'})
        if query.action == 'insert':
            return response([{**query.payload, 'id': f'{table}-inserted'}])
        if query.action == 'update':
            return response([{**query.payload, 'id': 'updated'}])
        return response([])

    monkeypatch.setattr(winner_service, '_safe_supabase', fake_safe)


def test_select_weighted_winner_returns_valid_winner(monkeypatch):
    install_winner_fakes(monkeypatch, [{'participant_id': 'participant-1', 'final_score': 80, 'is_eligible': True}])

    result = winner_service.select_weighted_winner('raffle-1')

    assert result['winner']['participant_id'] == 'participant-1'
    assert result['winner']['username'] == 'test_front'
    assert result['claim_status'] == 'confirmed'


def test_select_weighted_winner_without_eligible_participants_returns_controlled_error(monkeypatch):
    install_winner_fakes(monkeypatch, [])

    with pytest.raises(HTTPException) as error:
        winner_service.select_weighted_winner('raffle-1')

    assert error.value.status_code == 400
    assert 'No hay participantes elegibles' in error.value.detail
