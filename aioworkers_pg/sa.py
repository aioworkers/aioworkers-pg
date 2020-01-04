# true
from .base import Connector as BaseConnector


class Connector(BaseConnector):
    async def pool_factory(self, config):
        import asyncpgsa
        pool = await asyncpgsa.create_pool(
            config.dsn, init=self._init_connection,
        )
        self.logger.debug('Create pool with address %s', config.dsn)
        return pool

    async def _init_connection(self, connection):
        import json
        # TODO: Need general solution to add codecs
        # https://github.com/aioworkers/aioworkers-pg/issues/1
        # Add codecs for json.
        for t in ['json', 'jsonb']:
            await connection.set_type_codec(
                t,
                encoder=lambda x: x,
                decoder=json.loads,
                schema='pg_catalog',
            )
