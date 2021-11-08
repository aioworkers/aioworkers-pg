import pytest


@pytest.fixture
def config(config, dsn):
    config.update(
        db={
            "cls": "aioworkers_pg.base.Connector",
            "dsn": dsn,
            "pool": {
                "min_size": 1,
                "max_size": 1,
            },
        },
    )
    return config


async def test_custom_pool_setup(context):
    assert context.db._pool._minsize == 1
    assert context.db._pool._maxsize == 1
