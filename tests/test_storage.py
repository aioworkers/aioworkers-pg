import pytest


@pytest.fixture
def config(dsn):
    from aioworkers.core.config import Config
    return Config(
        db={
            'cls': 'aioworkers_pg.base.Connector',
            'dsn': dsn,
        },
        storage={
            'cls': 'aioworkers_pg.storage.RoStorage',
            'dsn': dsn,
            'table': 'x',
            'key': 'id',
            'format': 'dict',
        },
    )


async def test_ro_storage(context, recreate_table):
    await recreate_table('x', 'id serial', 'a text')
    v = await context.storage.get(1)
    assert v is None

    await context.db.execute('INSERT INTO x(a) VALUES ($1)', 'a')
    v = await context.storage.get(1)
    assert v == {'a': 'a', 'id': 1}
