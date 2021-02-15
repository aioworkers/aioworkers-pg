# aioworkers-pg

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioworkers-pg)
![PyPI](https://img.shields.io/pypi/v/aioworkers-pg)

Asyncpg plugin for `aioworkers`.


## Usage

Add this to aioworkers config.yaml:

```yaml
db:
  cls: aioworkers_pg.base.Connector
  dsn: postgresql:///test
```

You can get access to postgres anywhere via context:

```python
await context.db.execute('CREATE TABLE users(id serial PRIMARY KEY, name text)')
await context.db.execute(users.insert().values(name='Bob'))
```


## Storage

```yaml
storage:
  cls: aioworkers_pg.storage.RoStorage
  dsn: postgresql:///test
  table: mytable  # optional instead custom sql
  key: id
  get: SELECT * FROM mytable WHERE id = :id  # optional custom sql
  format: dict  # or row
```

## Development

Install dev requirements:

```shell
poetry install
```

Run postgres:

```shell
docker run --rm -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=test -d postgres
```

Run tests:

```shell
pytest
```
