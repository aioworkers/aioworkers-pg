from typing import Optional

import asyncpg
from aioworkers.core.config import ValueExtractor

from aioworkers_pg.abc import AbstractPGConnector


class Connector(AbstractPGConnector):
    _connect_kwargs: dict
    _pool: Optional[asyncpg.pool.Pool] = None

    def __init__(self, *args, **kwargs):
        self._pool = None
        self._connect_kwargs = {
            "init": self._default_connection_init,
        }
        super().__init__(*args, **kwargs)

    def set_config(self, config: ValueExtractor) -> None:
        cfg: ValueExtractor = config.new_parent(logger=__package__)
        super().set_config(cfg)

        connection_init: Optional[str] = self.config.get("connection.init")
        connection_setup: Optional[str] = self.config.get("connection.setup")
        connection_class: Optional[str] = self.config.get("connection.class")

        kwargs = dict(self.config.get("pool") or ())

        connection_init = kwargs.pop("init", connection_init)
        if connection_init:
            kwargs["init"] = self.context.get_object(connection_init)
        else:
            kwargs["init"] = self._default_connection_init

        connection_setup = kwargs.pop("setup", connection_setup)
        if connection_setup:
            kwargs["setup"] = self.context.get_object(connection_setup)

        connection_class = kwargs.pop("connection_class", connection_class)
        if connection_class:
            kwargs["connection_class"] = self.context.get_object(connection_class)

        record_class: Optional[str] = kwargs.pop("record_class", None)
        if record_class:
            kwargs["record_class"] = self.context.get_object(record_class)

        self._connect_kwargs = kwargs

    @property
    def pool(self) -> asyncpg.pool.Pool:
        assert self._pool
        return self._pool

    def __getattr__(self, attr):
        # Proxy all unresolved attributes to the wrapped Pool object.
        return getattr(self._pool, attr)

    async def connect(self):
        assert self._pool is None, "Already created pool"
        dsn = self._dsn
        self._pool = await asyncpg.create_pool(dsn, **self._connect_kwargs)
        if dsn:
            dsn = dsn.with_password("***")
        self.logger.debug("Create pool with address %s", dsn)

    async def disconnect(self):
        assert self._pool is not None, "Pool not created"
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
