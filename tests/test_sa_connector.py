import pytest
import sqlalchemy


@pytest.fixture
def config(config, dsn):
    config.update(
        db={
            "cls": "aioworkers_pg.sa.Connector",
            "dsn": dsn,
        },
    )
    return config


# @pytest.mark.skip(reason="Test hangs on Github Actions")
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

    async with context.db.engine.connect() as conn:
        await conn.run_sync(users.metadata.drop_all)
        await conn.run_sync(users.metadata.create_all)

        data = {"x": 1}
        await conn.execute(users.insert().values(name="Bob", data=data))
        await conn.execute(
            users.insert().values(
                [
                    {"name": "John"},
                    {"name": "Mike"},
                ]
            )
        )
        count = await conn.execute(sa.select(sa.func.count()).select_from(users))
        assert 3 == count.scalar()
        sql = users.select().where(users.c.id == 1)
        result: sa.CursorResult = await conn.execute(sql)
        user = dict(zip(sql.selected_columns.keys(), result.fetchone()))
        assert "Bob" == user["name"]
        assert data == user["data"]


async def test_execute(context):
    r = await context.db.execute(sqlalchemy.select(sqlalchemy.func.now()))
    assert 1 == r.rowcount


async def test_execute_str(context):
    r = await context.db.execute("SELECT now()")
    assert 1 == r.rowcount
