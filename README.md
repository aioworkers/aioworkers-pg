# aioworkers-pg


[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/aioworkers/aioworkers-pg/CI)](https://github.com/aioworkers/aioworkers-pg/actions?query=workflow%3ACI)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioworkers-pg)](https://pypi.org/project/aioworkers-pg)
[![PyPI](https://img.shields.io/pypi/v/aioworkers-pg)](https://pypi.org/project/aioworkers-pg)

Asyncpg plugin for `aioworkers`.


## Usage

### Connection

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

### Connection additional

```yaml
db:
  cls: aioworkers_pg.base.Connector
  dsn: postgresql:///test
  pool:
    min_size: 1
    max_size: 100
```


### Storage

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
