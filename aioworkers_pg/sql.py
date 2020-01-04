import re
from collections import ChainMap
from typing import Any, Match, Sequence


NAME = re.compile(r'[^:]:([\d\w_]+)')


class Table:
    def __init__(self, name):
        self.name = name

    def select(self, *fields, **where):
        sql = ['SELECT']
        if fields:
            sql.append(', '.join(fields))
        else:
            sql.append('*')
        sql.extend(('FROM', self.name))
        if where:
            sql.append('WHERE')
            sql.append(' AND '.join(' = '.join((k, ':' + k)) for k in where))
        return SQL(' '.join(sql), **where)


class SQL:
    __slots__ = ('_sql', '_compiled', '_args', '_data')

    def __init__(self, sql, *compiled, **kwargs):
        self._sql = sql
        self._compiled = compiled or self._get_params(sql)
        self._args = self._get_args(kwargs) if kwargs else (self._compiled[0],)
        self._data = kwargs

    def with_data(self, *args, **kwargs):
        m = ChainMap(kwargs, *reversed(args), self._data)
        cls = type(self)
        return cls(self._sql, *self._compiled, **m)

    @staticmethod
    def _get_params(sql: str) -> Sequence[Any]:
        result = [sql]
        pos = {}  # type: dict

        def repl(m: Match) -> str:
            name = m.group(1)
            if name in pos:
                position = pos[name]
            else:
                position = pos.setdefault(name, len(result))
                result.append(name)
            return m.group(0).replace(':' + name, '${}'.format(position))

        result[0] = NAME.sub(repl, sql)
        return tuple(result)

    def _get_args(self, data):
        args = [data.get(k) for i, k in enumerate(self._compiled)]
        args[0] = self._compiled[0]
        return tuple(args)

    def __repr__(self):
        return self._sql

    def __iter__(self):
        yield from self._args

    def __len__(self):
        return len(self._args)
