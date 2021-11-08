import pytest
from aioworkers.utils import import_uri


async def custom_setup(connection):
    pass


@pytest.fixture
def config(config, dsn):
    config.update(
        db={
            "cls": "aioworkers_pg.base.Connector",
            "dsn": dsn,
            "pool": {
                "setup": import_uri(custom_setup),
            },
        },
    )
    return config


async def test_custom_pool_setup(context):
    await context.db.execute("SELECT 1")
