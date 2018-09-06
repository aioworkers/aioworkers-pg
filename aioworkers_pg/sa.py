from .base import Connector as BaseConnector


class Connector(BaseConnector):

    async def _create_pool(self):
        import asyncpgsa
        return await asyncpgsa.create_pool(self.config.dsn)
