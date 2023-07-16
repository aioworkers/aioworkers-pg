from typing import Optional

import pytest
from aioworkers.utils import import_uri
from asyncpg.connection import Connection
from asyncpg.protocol.protocol import Record


class CustomConnection(Connection):
    async def execute(self, query: str, *args, timeout: Optional[float] = None) -> str:
        query += "SELECT 1"
        return await super().execute(query, *args, timeout=timeout)


class CustomRecord(Record):
    pass


@pytest.fixture
def config(config, dsn):
    config.update(
        db={
            "cls": "aioworkers_pg.base.Connector",
            "dsn": dsn,
            "pool": {
                "connection_class": import_uri(CustomConnection),
                "record_class": import_uri(CustomRecord),
            },
        },
    )
    return config


async def test_custom_classes(context):
    # Run an empty query. The final query will be updated in the CustomConnection.
    await context.db.execute("")
