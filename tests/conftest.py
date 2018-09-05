import pytest
from aioworkers.core.config import Config
from aioworkers.core.context import Context


@pytest.fixture
def config():
    return Config(
        db={
            'cls': 'aioworkers_pg.base.Connector',
            'dsn': 'postgresql://localhost/test',
        }
    )


@pytest.fixture
def context(config, loop):
    with Context(config, loop=loop) as ctx:
        return ctx
