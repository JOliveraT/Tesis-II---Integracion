from copy import deepcopy
from datetime import datetime, timezone
from types import SimpleNamespace
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import (
    auth_service,
    participant_service,
    scoring_service,
    twitch_chat_service,
    winner_service,
)

client = TestClient(app)

RAFFLE_ID = "11111111-1111-1111-1111-111111111111"
USER_ID = "user-test-001"
CHANNEL_ID = "channel-test-001"
FAKE_USER = {"id": USER_ID, "email": "test@example.com"}


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


class IntegrationFakeQuery:
    def __init__(self, supabase, table_name, action="select", payload=None):
        self.supabase = supabase
        self.table_name = table_name
        self.action = action
        self.payload = payload
        self.filters = []
        self.selected = "*"
        self.orders = []
        self.limit_count = None
        self.single_row = False

    def select(self, columns="*"):
        self.action = "select"
        self.selected = columns
        return self

    def insert(self, payload):
        self.action = "insert"
        self.payload = payload
        return self

    def update(self, payload):
        self.action = "update"
        self.payload = payload
        return self

    def delete(self):
        self.action = "delete"
        return self

    def eq(self, column, value):
        self.filters.append(("eq", column, value))
        return self

    def neq(self, column, value):
        self.filters.append(("neq", column, value))
        return self

    def in_(self, column, values):
        self.filters.append(("in", column, tuple(values)))
        return self

    def order(self, column, desc=False):
        self.orders.append((column, desc))
        return self

    def limit(self, count):
        self.limit_count = count
        return self

    def single(self):
        self.single_row = True
        return self

    def execute(self):
        return self.supabase.execute(self)


class IntegrationFakeSupabase:
    def __init__(self):
        self.tables = {
            "twitch_channels": [
                {
                    "id": CHANNEL_ID,
                    "user_id": USER_ID,
                    "twitch_user_id": "streamer-twitch-test-001",
                    "updated_at": _now_iso(),
                }
            ],
            "raffles": [
                {
                    "id": RAFFLE_ID,
                    "channel_id": CHANNEL_ID,
                    "command": "!sorteo",
                    "status": "active",
                    "confirmation_mode": "instant",
                    "created_at": _now_iso(),
                    "updated_at": _now_iso(),
                }
            ],
            "participants": [],
            "raffle_participants": [],
            "participation_entries": [],
            "chat_messages": [],
            "channel_point_redemptions": [],
            "participation_scores": [],
            "raffle_results": [],
            "audit_logs": [],
        }
        self._ids = {table: 0 for table in self.tables}

    def table(self, table_name):
        self.tables.setdefault(table_name, [])
        self._ids.setdefault(table_name, 0)
        return IntegrationFakeQuery(self, table_name)

    def execute(self, query):
        if query.action == "select":
            return SimpleNamespace(data=self._select(query))
        if query.action == "insert":
            return SimpleNamespace(data=self._insert(query))
        if query.action == "update":
            return SimpleNamespace(data=self._update(query))
        if query.action == "delete":
            return SimpleNamespace(data=self._delete(query))
        return SimpleNamespace(data=[])

    def _select(self, query):
        rows = [deepcopy(row) for row in self.tables[query.table_name] if self._matches(row, query.filters)]

        for column, desc in reversed(query.orders):
            rows.sort(key=lambda row: row.get(column) or "", reverse=desc)

        if query.limit_count is not None:
            rows = rows[: query.limit_count]

        if query.table_name == "raffle_participants" and "participants:participant_id" in (query.selected or ""):
            rows = [self._with_participant_relation(row) for row in rows]

        if query.single_row:
            return rows[0] if rows else None
        return rows

    def _insert(self, query):
        payloads = query.payload if isinstance(query.payload, list) else [query.payload]
        inserted = []
        for payload in payloads:
            row = deepcopy(payload)
            row.setdefault("id", self._next_id(query.table_name))
            if query.table_name == "raffle_participants":
                row.setdefault("joined_at", _now_iso())
                row.setdefault("is_eligible", False)
                row.setdefault("final_score", 0)
            if query.table_name == "participants":
                row.setdefault("created_at", _now_iso())
            self.tables[query.table_name].append(row)
            inserted.append(deepcopy(row))
        return inserted

    def _update(self, query):
        updated = []
        for row in self.tables[query.table_name]:
            if self._matches(row, query.filters):
                row.update(deepcopy(query.payload))
                updated.append(deepcopy(row))
        return updated

    def _delete(self, query):
        kept = []
        deleted = []
        for row in self.tables[query.table_name]:
            if self._matches(row, query.filters):
                deleted.append(deepcopy(row))
            else:
                kept.append(row)
        self.tables[query.table_name] = kept
        return deleted

    def _next_id(self, table_name):
        self._ids[table_name] += 1
        return f"{table_name}-{self._ids[table_name]}"

    def _matches(self, row, filters):
        for op, column, value in filters:
            current = row.get(column)
            if op == "eq" and current != value:
                return False
            if op == "neq" and current == value:
                return False
            if op == "in" and current not in value:
                return False
        return True

    def _with_participant_relation(self, row):
        enriched = deepcopy(row)
        participant = next(
            (item for item in self.tables["participants"] if item["id"] == row.get("participant_id")),
            {},
        )
        enriched["participants"] = deepcopy(participant)
        return enriched

    def participant_usernames(self):
        return [participant["username"] for participant in self.tables["participants"]]

    def raffle_participant_ids(self, raffle_id=RAFFLE_ID):
        return [
            row["participant_id"]
            for row in self.tables["raffle_participants"]
            if row["raffle_id"] == raffle_id and row.get("status") != "removed"
        ]

    def participation_entries_for_event(self, message_id):
        return [row for row in self.tables["participation_entries"] if row.get("source_event_id") == message_id]


@pytest.fixture
def fake_supabase(monkeypatch):
    fake = IntegrationFakeSupabase()
    for module in (participant_service, scoring_service, twitch_chat_service, winner_service):
        monkeypatch.setattr(module, "supabase", fake)
    monkeypatch.setattr(
        twitch_chat_service,
        "create_audit_log",
        lambda **kwargs: fake.table("audit_logs").insert(kwargs).execute().data[0],
    )
    app.dependency_overrides[auth_service.get_current_user] = lambda: FAKE_USER
    yield fake
    app.dependency_overrides.clear()


def send_test_message(
    message_id,
    twitch_user_id="viewer-int-001",
    username="viewer_int_001",
    display_name="Viewer Int 001",
):
    return client.post(
        "/twitch/chat/test-message",
        json={
            "message_id": message_id,
            "twitch_user_id": twitch_user_id,
            "username": username,
            "display_name": display_name,
            "message_text": "!sorteo",
        },
    )


# PI-BE-01: valida que un mensaje simulado de Twitch registre al participante por API.
def test_twitch_test_message_registers_participant(fake_supabase):
    response = send_test_message("msg-int-001")

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Mensaje procesado correctamente"
    assert body["data"]["participant_registered"] is True
    assert body["data"]["entry_created"] is True
    assert body["data"]["duplicate_event"] is False
    assert "viewer_int_001" in fake_supabase.participant_usernames()


# PI-BE-02: valida idempotencia cuando llega dos veces el mismo evento de Twitch.
def test_twitch_test_message_duplicate_event_is_idempotent(fake_supabase):
    first_response = send_test_message("msg-int-duplicate")
    second_response = send_test_message("msg-int-duplicate")

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert second_response.json()["data"]["duplicate_event"] is True
    assert len(fake_supabase.participation_entries_for_event("msg-int-duplicate")) == 1


# PI-BE-03: valida que un mismo viewer con mensajes distintos no duplique raffle_participants.
def test_same_viewer_second_message_does_not_duplicate_raffle_participant(fake_supabase):
    first_response = send_test_message("msg-int-002")
    second_response = send_test_message("msg-int-003")

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    participant_ids = fake_supabase.raffle_participant_ids()
    assert len(participant_ids) == 1
    assert len(set(participant_ids)) == 1


# PI-BE-04: valida que el listado API del sorteo devuelva viewers registrados sin duplicados.
def test_list_raffle_participants_returns_registered_viewers(fake_supabase):
    send_test_message(
        "msg-int-list-001",
        twitch_user_id="viewer-list-001",
        username="viewer_list_001",
        display_name="Viewer List 001",
    )
    send_test_message(
        "msg-int-list-002",
        twitch_user_id="viewer-list-001",
        username="viewer_list_001",
        display_name="Viewer List 001",
    )
    send_test_message(
        "msg-int-list-003",
        twitch_user_id="viewer-list-002",
        username="viewer_list_002",
        display_name="Viewer List 002",
    )

    response = client.get(f"/participants/raffle/{RAFFLE_ID}")

    assert response.status_code == 200
    participants = response.json()["data"]
    usernames = [participant["username"] for participant in participants]
    assert "viewer_list_001" in usernames
    assert "viewer_list_002" in usernames
    assert len(usernames) == len(set(usernames))


# PI-BE-05: valida cálculo de scoring y selección de un ganador elegible por API.
def test_scoring_and_winner_flow_returns_valid_winner(fake_supabase):
    viewers = [
        ("msg-int-score-001", "viewer-score-001", "viewer_score_001", "Viewer Score 001"),
        ("msg-int-score-002", "viewer-score-002", "viewer_score_002", "Viewer Score 002"),
        ("msg-int-score-003", "viewer-score-003", "viewer_score_003", "Viewer Score 003"),
    ]
    for message_id, twitch_user_id, username, display_name in viewers:
        response = send_test_message(
            message_id,
            twitch_user_id=twitch_user_id,
            username=username,
            display_name=display_name,
        )
        assert response.status_code == 200

    scoring_response = client.post(f"/scoring/calculate/{RAFFLE_ID}")
    winner_response = client.post(f"/winner/select/{RAFFLE_ID}")

    assert scoring_response.status_code == 200
    scoring_body = scoring_response.json()
    assert scoring_body["participants_evaluated"] == 3

    assert winner_response.status_code == 200
    winner = winner_response.json()["winner"]
    eligible_ids = set(fake_supabase.raffle_participant_ids())
    assert winner["participant_id"] in eligible_ids
    assert winner["username"] in {"viewer_score_001", "viewer_score_002", "viewer_score_003"}
