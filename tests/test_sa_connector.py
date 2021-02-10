import pytest


@pytest.fixture
def config(config, dsn):
    print("Step config")
    config.update(
        db={
            "cls": "aioworkers_pg.sa.Connector",
            "dsn": dsn,
        },
    )
    return config


async def test_sa_connector(context):
    """
    Test common asyncpg pool methods which were bind to connector.
    """
    import sqlalchemy as sa

    users = sa.Table(
        "users",
        sa.MetaData(),
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.VARCHAR(255)),
        sa.Column("data", sa.JSON()),
    )
    print("Step 1")
    # Could not run DropTable(users) or CreateTable(users) because an error during compile
    # https://github.com/CanopyTax/asyncpgsa/issues/93
    await context.db.execute("DROP TABLE IF EXISTS users;")
    await context.db.execute(
        "CREATE TABLE users(id serial PRIMARY KEY, name text, data json)"
    )

    data = {"x": 1}
    await context.db.execute(users.insert().values(name="Bob", data=data))
    await context.db.execute(
        users.insert().values(
            [
                {"name": "John"},
                {"name": "Mike"},
            ]
        )
    )
    count = await context.db.fetchval(users.count())
    assert 3 == count

    user = await context.db.fetchrow(users.select().where(users.c.id == 1))
    assert "Bob" == user["name"]
    assert data == user["data"]

    r = [i for i in await context.db.fetch(users.select())]
    assert 3 == len(r)
    print("Before Close")

    await context.db.close()
    # Check that method available
    context.db.terminate()
