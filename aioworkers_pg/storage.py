from aioworkers.storage.base import AbstractStorageReadOnly

# true
from .base import Connector
from .formatter import PGFormattedEntity
from .sql import SQL, Table


class RoStorage(PGFormattedEntity, Connector, AbstractStorageReadOnly):
    def __init__(self, *args, **kwargs):
        self._key = ''
        self._table = None
        self._get_sql = None
        super().__init__(*args, **kwargs)

    def set_config(self, config):
        super().set_config(config)
        self._key = self.config.key
        self._table = self.config.get('table') and Table(self.config.table)
        get_sql = self.config.get('get')
        if get_sql:
            self._get_sql = SQL(get_sql)
        else:
            self._get_sql = self._table.select(**{self._key: None})

    async def init(self):
        await Connector.init(self)

    def raw_key(self, key):
        return self._get_sql.with_data({self._key: key})

    async def get(self, key):
        result = await self._pool.fetchrow(*self.raw_key(key))
        if result:
            return self.decode(result)
