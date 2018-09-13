async def test_pool_close(loop):
    from aioworkers.core.context import Context
    from aioworkers.core.config import Config
    conf = Config(
        db={
            'cls': 'aioworkers_pg.base.Connector',
            'dsn': 'postgresql://localhost/test',
        },
    )
    c = Context(conf, loop=loop)
    await c.init()
    await c.start()
    assert not c.db._pool._closed
    await c.stop()
    assert c.db._pool._closed
