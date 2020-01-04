import asyncpg
from aioworkers.core.base import AbstractConnector


class Connector(AbstractConnector):
    def __init__(self, *args, **kwargs):
        self._pool = None
        super().__init__(*args, **kwargs)

    def set_config(self, config):
        cfg = config.new_parent(logger='aioworkers_pg')
        super().set_config(cfg)

    @property
    def pool(self) -> asyncpg.pool.Pool:
        assert self._pool
        return self._pool

    def __getattr__(self, attr):
        # Proxy all unresolved attributes to the wrapped Pool object.
        return getattr(self._pool, attr)

    async def connect(self):
        if self._pool is None:
            self._pool = await self.pool_factory(self.config)

    async def pool_factory(self, config):
        pool = await asyncpg.create_pool(
            config.dsn, init=self._init_connection,
        )
        self.logger.debug('Create pool with address %s', config.dsn)
        return pool

    async def disconnect(self):
        if self._pool is not None:
            self.logger.debug('Close pool')
            await self._pool.close()
            self._pool = None

    async def _init_connection(self, connection):
        import json
        # TODO: Need general solution to add codecs
        # https://github.com/aioworkers/aioworkers-pg/issues/1
        # Add codecs for json.
        for t in ['json', 'jsonb']:
            await connection.set_type_codec(
                t,
                encoder=json.dumps,
                decoder=json.loads,
                schema='pg_catalog',
            )
