async def test_pool_close(loop, dsn):
    from aioworkers.core.context import Context
    from aioworkers.core.config import Config
    conf = Config(
        db={
            'cls': 'aioworkers_pg.base.Connector',
            'dsn': dsn,
        },
    )
    async with Context(conf, loop=loop) as c:
        assert c.db._pool is not None
        assert not c.db._pool._closed
    assert c.db._pool is None
