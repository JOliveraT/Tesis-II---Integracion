import os
from types import SimpleNamespace

os.environ.setdefault('SUPABASE_URL', 'https://unit-test.supabase.co')
os.environ.setdefault('SUPABASE_SERVICE_ROLE_KEY', 'unit-test-service-role-key')


class FakeQuery:
    def __init__(self, table_name, action='select', payload=None):
        self.table_name = table_name
        self.action = action
        self.payload = payload
        self.filters = []
        self.selected = None
        self.orders = []
        self.limit_count = None
        self.single_row = False

    def select(self, columns='*'):
        self.action = 'select'
        self.selected = columns
        return self

    def insert(self, payload):
        self.action = 'insert'
        self.payload = payload
        return self

    def update(self, payload):
        self.action = 'update'
        self.payload = payload
        return self

    def delete(self):
        self.action = 'delete'
        return self

    def eq(self, column, value):
        self.filters.append(('eq', column, value))
        return self

    def neq(self, column, value):
        self.filters.append(('neq', column, value))
        return self

    def in_(self, column, values):
        self.filters.append(('in', column, tuple(values)))
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


class FakeSupabase:
    def table(self, table_name):
        return FakeQuery(table_name)


def response(data=None):
    return SimpleNamespace(data=[] if data is None else data)


def filters_dict(query):
    return {(op, column): value for op, column, value in query.filters}
