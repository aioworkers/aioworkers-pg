import pytest

from aioworkers_pg.sql import SQL, Table


@pytest.fixture
def config(config, dsn):
    config.update(
        db={
            "cls": "aioworkers_pg.base.Connector",
            "dsn": dsn,
        },
    )
    return config


async def test_select(context, recreate_table):
    await recreate_table("x", "a text")
    sql = Table("x").select("a", a="q")
    assert list(sql) == ["SELECT a FROM x WHERE a = $1", "q"]
    await context.db.fetch(*sql)
    sql = Table("x").select()
    assert list(sql) == ["SELECT * FROM x"]
    await context.db.fetch(*sql)


def test_sql1():
    sql = SQL("SELECT :p")
    assert sql._compiled == ("SELECT $1", "p")
    assert list(sql) == ["SELECT $1"]

    sql = sql.with_data(p=1)
    assert sql._compiled == ("SELECT $1", "p")
    assert list(sql) == ["SELECT $1", 1]
    assert repr(sql) == "SELECT :p"

    sql = sql.with_data({"p": 1})
    assert sql._compiled == ("SELECT $1", "p")
    assert list(sql) == ["SELECT $1", 1]
    assert repr(sql) == "SELECT :p"

    sql = sql.with_data({"p": 1}, p=2)
    assert list(sql) == ["SELECT $1", 2]


async def test_sql2(context):
    sql = SQL("SELECT :p::int, :p", p=1)
    assert sql._compiled == ("SELECT $1::int, $1", "p")
    assert list(sql) == ["SELECT $1::int, $1", 1]
    await context.db.fetchrow(*sql)


async def test_sql3(context, recreate_table):
    await recreate_table("reports")
    sql = SQL("SELECT * FROM reports", p=1)
    assert sql._compiled == ("SELECT * FROM reports",)
    assert list(sql) == ["SELECT * FROM reports"]
    await context.db.fetchrow(*sql)
