from typing import Awaitable, Callable, Optional, Type

import asyncpg
import warnings
from aioworkers.core.base import AbstractConnector
from aioworkers.core.config import ValueExtractor


class Connector(AbstractConnector):
    _pool_init: Optional[Callable[[asyncpg.Connection], Awaitable]] = None
    _pool_setup: Optional[Callable[[asyncpg.Connection], Awaitable]] = None
    _connection_class: Optional[
        Type[asyncpg.connection.Connection]
    ] = asyncpg.connection.Connection
    _record_class: type = asyncpg.protocol.Record
    _connect_kwargs: dict = {}

    def __init__(self, *args, **kwargs):
        self._pool = None
        self._pool_init = self._default_pool_init
        super().__init__(*args, **kwargs)

    def set_config(self, config: ValueExtractor) -> None:
        cfg = config.new_parent(logger=__package__)
        super().set_config(cfg)

        # TODO: Remove deprecated code.
        if self.config.get("connection.init"):
            warnings.warn(
                "Do not use connection.init config. Use pool.init", DeprecationWarning
            )
            self._pool_init = self.context.get_object(
                self.config.get("connection.init")
            )

        pool_config = dict(self.config.get("pool", {}))
        if not pool_config:
            # Do not process pool config if there is no any parameter
            return

        pool_init: Optional[str] = pool_config.pop("init", None)
        if pool_init:
            self._pool_init = self.context.get_object(pool_init)

        pool_setup: Optional[str] = pool_config.pop("setup", None)
        if pool_setup:
            self._pool_setup = self.context.get_object(pool_setup)

        connection_class: Optional[str] = pool_config.pop("connection_class", None)
        if connection_class:
            self._connection_class = self.context.get_object(connection_class)

        record_class: Optional[str] = pool_config.pop("record_class", None)
        if record_class:
            self._record_class = self.context.get_object(record_class)

        self._connect_kwargs = pool_config

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
            init=self._pool_init,
            setup=self._pool_setup,
            connection_class=self._connection_class,
            record_class=self._record_class,
            **self._connect_kwargs,
        )
        self.logger.debug("Create pool with address %s", config.dsn)
        return pool

    async def disconnect(self):
        if self._pool is not None:
            self.logger.debug("Close pool")
            await self._pool.close()
            self._pool = None

    async def _default_pool_init(self, connection: asyncpg.Connection):
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
