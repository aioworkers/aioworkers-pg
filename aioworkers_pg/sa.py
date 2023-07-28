from typing import Union

from aioworkers.core.base import AbstractConnector
from sqlalchemy import CursorResult, Executable, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class Connector(AbstractConnector):
    engine: AsyncEngine

    async def connect(self):
        dsn = self.config.get_uri("dsn")
        dsn = dsn.with_scheme("postgresql+asyncpg")

        self.engine = create_async_engine(
            dsn,
            echo=True,
        )

        self.logger.debug("Create engine with dsn %s", dsn.with_password("***"))

    async def disconnect(self):
        await self.engine.dispose()

    async def execute(self, statement: Union[str, Executable], *args, **kwargs) -> CursorResult:
        async with self.engine.connect() as conn:
            if isinstance(statement, str):
                statement = text(statement)
            return await conn.execute(statement, *args, **kwargs)
