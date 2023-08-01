from typing import Optional, Union

from aioworkers.net.uri import URI
from sqlalchemy import CursorResult, Executable, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from aioworkers_pg.abc import AbstractPGConnector


class Connector(AbstractPGConnector):
    _default_scheme: str = "postgresql+asyncpg"
    _default_dsn = URI(f"{_default_scheme}:///")
    _engine: Optional[AsyncEngine] = None

    async def connect(self):
        assert self._engine is None, "Engine already created"

        dsn = self._dsn
        if dsn:
            dsn = dsn.with_scheme(self._default_scheme)
        else:
            dsn = self._default_dsn

        self._engine = create_async_engine(
            dsn,
            echo=True,
        )

        self.logger.debug("Create engine with dsn %s", dsn.with_password("***"))

    async def disconnect(self):
        assert self._engine is not None, "Engine not created"
        await self._engine.dispose()
        self._engine = None

    @property
    def engine(self) -> AsyncEngine:
        assert self._engine
        return self._engine

    async def execute(self, statement: Union[str, Executable], *args, **kwargs) -> CursorResult:
        assert self._engine
        async with self._engine.connect() as conn:
            if isinstance(statement, str):
                statement = text(statement)
            return await conn.execute(statement, *args, **kwargs)
