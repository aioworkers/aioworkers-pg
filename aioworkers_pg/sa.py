from .base import Connector as BaseConnector


class Connector(BaseConnector):

    async def _create_pool(self):
        import asyncpgsa
        return await asyncpgsa.create_pool(self.config.dsn, init=self._init_connection)

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
