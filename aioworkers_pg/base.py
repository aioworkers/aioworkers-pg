from typing import Awaitable, Callable, Optional

import asyncpg
from aioworkers.core.base import AbstractConnector
from aioworkers.core.config import ValueExtractor


class Connector(AbstractConnector):
    _connection_init: Optional[Callable[[asyncpg.Connection], Awaitable]]

    def __init__(self, *args, **kwargs):
        self._pool = None
        super().__init__(*args, **kwargs)

    def set_config(self, config: ValueExtractor) -> None:
        cfg = config.new_parent(logger=__package__)
        super().set_config(cfg)
        connection_init: Optional[str] = self.config.get(
            "connection.init",
        )
        if connection_init:
            self._connection_init = self.context.get_object(connection_init)
        else:
            self._connection_init = self._default_connection_init

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

    async def pool_factory(self, config) -> asyncpg.pool.Pool:
        pool = await asyncpg.create_pool(
            config.dsn,
            init=self._connection_init,
        )
        self.logger.debug("Create pool with address %s", config.dsn)
        return pool

    async def disconnect(self):
        if self._pool is not None:
            self.logger.debug("Close pool")
            await self._pool.close()
            self._pool = None

    async def _default_connection_init(self, connection: asyncpg.Connection):
        import json

        # TODO: Need general solution to add codecs
        # https://github.com/aioworkers/aioworkers-pg/issues/1
        # Add codecs for json.
        for t in ["json", "jsonb"]:
            await connection.set_type_codec(
                t,
                encoder=json.dumps,
                decoder=json.loads,
                schema="pg_catalog",
            )
