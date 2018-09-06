import pytest


@pytest.fixture
def config():
    from aioworkers.core.config import Config
    return Config(
        db={
            'cls': 'aioworkers_pg.base.Connector',
            'dsn': 'postgresql://localhost/test',
        },
    )


async def test_connector(context):
    """
    Test common asyncpg pool methods which were bind to connector.
    """
    await context.db.execute('''
    DROP TABLE IF EXISTS users;
    CREATE TABLE users(id serial PRIMARY KEY, name text);
    ''')

    await context.db.execute('''INSERT INTO users(name) VALUES($1)''', 'Bob')

    await context.db.executemany('''INSERT INTO users(name) VALUES($1)''', [
        ('John',),
        ('Mike',),
    ])

    r = await context.db.fetchval('''SELECT COUNT(*) FROM users''')
    assert 3 == r

    r = await context.db.fetchrow('''SELECT * FROM users WHERE id=1''')
    assert 1 == r['id']
    assert 'Bob' == r['name']

    r = await context.db.fetch('''SELECT * FROM users''')
    assert 3 == len(r)

    connection = await context.db.acquire()
    try:
        await connection.execute('''DROP TABLE users''')
    finally:
        await context.db.release(connection)

    await context.db.close()
    context.db.terminate()
