import pytest
from aioworkers.net.uri import URI

from aioworkers_pg.base import Connector


@pytest.fixture
def config(config, dsn):
    uri = URI(dsn)
    port = uri.port or 5432  # type: ignore # https://github.com/aioworkers/aioworkers/pull/202
    database = (uri.path or "").strip("/")  # type: ignore
    config.update(
        db={
            "name": "db",
            "cls": "aioworkers_pg.base.Connector",
            "username": uri.username,
            "password": uri.password,
            "host": uri.hostname,
            "database": database,
            "port": port,
        },
    )
    return config


def test_dsn(config, dsn):
    c = Connector()
    c.set_config(config.db)
    assert str(c._dsn) == dsn


async def test_connector(context, dsn):
    """
    Test common asyncpg pool methods which were bind to connector.
    """
    await context.db.execute(
        """
    DROP TABLE IF EXISTS users;
    CREATE TABLE users(id serial PRIMARY KEY, name text, data jsonb);
    """
    )

    await context.db.execute("INSERT INTO users(name, data) VALUES($1, $2)", "Bob", {"x": 1})

    await context.db.executemany(
        """INSERT INTO users(name) VALUES($1)""",
        [
            ("John",),
            ("Mike",),
        ],
    )

    r = await context.db.fetchval("""SELECT COUNT(*) FROM users""")
    assert 3 == r

    r = await context.db.fetchrow("""SELECT * FROM users WHERE id=1""")
    assert 1 == r["id"]
    assert "Bob" == r["name"]
    assert {"x": 1} == r["data"]

    r = await context.db.fetch("""SELECT * FROM users""")
    assert 3 == len(r)

    connection = await context.db.acquire()
    try:
        await connection.execute("""DROP TABLE users""")
    finally:
        await context.db.release(connection)

    await context.db.close()

    # Check that method available
    context.db.terminate()
