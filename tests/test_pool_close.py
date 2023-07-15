from aioworkers.core.config import Config
from aioworkers.core.context import Context


async def test_pool_close(dsn):
    conf = Config(
        db={
            "cls": "aioworkers_pg.base.Connector",
            "dsn": dsn,
        },
    )
    async with Context(conf) as c:
        assert c.db._pool is not None
        assert not c.db._pool._closed
    assert c.db._pool is None
