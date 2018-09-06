import pytest


@pytest.fixture
def config():
    from aioworkers.core.config import Config
    return Config(
        db={
            'cls': 'aioworkers_pg.sa.Connector',
            'dsn': 'postgresql://localhost/test',
        },
    )


async def test_sa_connector(context):
    """
    Test common asyncpg pool methods which were bind to connector.
    """
    import sqlalchemy as sa
    users = sa.Table(
        'users', sa.MetaData(),
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.VARCHAR(255)),
    )

    # Could not run DropTable(users) or CreateTable(users) because an error during compile
    await context.db.execute('DROP TABLE IF EXISTS users;')
    await context.db.execute('CREATE TABLE users(id serial PRIMARY KEY, name text)')

    await context.db.execute(users.insert().values(name='Bob'))
    await context.db.execute(users.insert().values([
        {'name': 'John'},
        {'name': 'Mike'},
    ]))
    count = await context.db.fetchval(users.count())
    assert 3 == count

    user = await context.db.fetchrow(users.select().where(users.c.id == 2))
    assert 'John' == user['name']

    r = [i for i in await context.db.fetch(users.select())]
    assert 3 == len(r)

    await context.db.close()
    context.db.terminate()
