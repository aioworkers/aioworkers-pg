import pytest


@pytest.fixture
def config():
    from aioworkers.core.config import Config
    return Config(
        db={
            'cls': 'aioworkers_pg.base.Connector',
            'dsn': 'postgresql://localhost/test',
        }
    )


@pytest.fixture
def context(config, loop):
    from aioworkers.core.context import Context
    with Context(config, loop=loop) as ctx:
        return ctx
