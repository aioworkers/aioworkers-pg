import pytest


@pytest.fixture
def context(config, loop):
    from aioworkers.core.context import Context
    with Context(config, loop=loop) as ctx:
        yield ctx
