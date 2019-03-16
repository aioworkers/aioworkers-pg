
import logging

import asyncpg
from aioworkers.core.base import AbstractEntity

logger = logging.getLogger('aioworkers_pg')


class Connector(AbstractEntity):
    # Method from pool which will be bind to connector
    __bind_methods = (
        'execute',
        'executemany',
        'fetch',
        'fetchval',
        'fetchrow',
        'acquire',
        'release',
        'close',
        'release',
        'terminate',
    )

    def __init__(self, config=None, *, context=None, loop=None):
        super().__init__(config, context=context, loop=loop)
        self._pool = None
        self.context.on_stop.append(self.stop)

    async def stop(self):
        await self._pool.close()

    async def _create_pool(self):
        return await asyncpg.create_pool(self.config.dsn, init=self._init_connection)

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

    async def init(self):
        await super().init()
        self._pool = await self._create_pool()
        for method_name in self.__bind_methods:
            f = getattr(self._pool, method_name)
            if f:
                setattr(self, method_name, f)
