import asyncpg
from aioworkers.core.config import ValueExtractor

# true
from .base import Connector as BaseConnector


class Connector(BaseConnector):
    async def pool_factory(self, config: ValueExtractor) -> asyncpg.pool.Pool:
        import asyncpgsa

        pool = await asyncpgsa.create_pool(
            config.dsn,
            init=self._pool_init,
        )
        self.logger.debug("Create pool with address %s", config.dsn)
        return pool

    async def _default_pool_init(self, connection: asyncpg.Connection):
        import json

        # TODO: Need general solution to add codecs
        # https://github.com/aioworkers/aioworkers-pg/issues/1
        # Add codecs for json.
        for t in ["json", "jsonb"]:
            await connection.set_type_codec(
                t,
                encoder=lambda x: x,
                decoder=json.loads,
                schema="pg_catalog",
            )
