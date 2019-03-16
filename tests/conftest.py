import os

import pytest


@pytest.fixture(scope='session')
def dsn():
    return os.environ.get('PG_DSN', 'postgresql://localhost/test')


@pytest.fixture
def context(config, loop):
    from aioworkers.core.context import Context
    with Context(config, loop=loop) as ctx:
        yield ctx


@pytest.fixture
def recreate_table(context):
    async def recreate_table(name, *fields):
        await context.db.execute('DROP TABLE IF EXISTS {}'.format(name))
        await context.db.execute('CREATE TABLE {} ({})'.format(name, ','.join(fields)))
    return recreate_table
