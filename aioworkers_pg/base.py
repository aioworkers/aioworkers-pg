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

    async def _create_pool(self):
        return await asyncpg.create_pool(self.config.dsn)

    async def init(self):
        self._pool = await self._create_pool()
        for method_name in self.__bind_methods:
            f = getattr(self._pool, method_name)
            if f:
                setattr(self, method_name, f)
