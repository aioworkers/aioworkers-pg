import pytest


@pytest.fixture
def config(config, dsn):
    config.update(
        db={
            "cls": "aioworkers_pg.base.Connector",
            "dsn": dsn,
        },
    )
    return config


async def test_connector(context):
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
