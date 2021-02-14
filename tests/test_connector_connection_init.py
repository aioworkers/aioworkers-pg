import asyncpg
import pytest
from aioworkers.utils import import_uri


async def custom_init(connection):
    pass


@pytest.fixture
def config(config, dsn):
    config.update(
        db={
            "cls": "aioworkers_pg.base.Connector",
            "dsn": dsn,
            "connection": {
                "init": import_uri(custom_init),
            },
        },
    )
    return config


async def test_custom_connection_init(context):
    await context.db.execute("SELECT 1")

    with pytest.raises(asyncpg.exceptions.DataError):
        await context.db.execute(
            "SELECT $1",
            {"x": 1},
        )
