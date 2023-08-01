aioworkers-pg
=============

.. image:: https://img.shields.io/pypi/v/aioworkers-pg.svg
  :target: https://pypi.org/project/aioworkers-pg

.. image:: https://github.com/aioworkers/aioworkers-pg/workflows/Tests/badge.svg
  :target: https://github.com/aioworkers/aioworkers-pg/actions?query=workflow%3ATests

.. image:: https://codecov.io/gh/aioworkers/aioworkers-pg/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/aioworkers/aioworkers-pg
  :alt: Coverage

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json
  :target: https://github.com/charliermarsh/ruff
  :alt: Code style: ruff

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :target: https://github.com/psf/black
  :alt: Code style: black

.. image:: https://img.shields.io/badge/types-Mypy-blue.svg
  :target: https://github.com/python/mypy
  :alt: Code style: Mypy

.. image:: https://readthedocs.org/projects/aioworkers-pg/badge/?version=latest
  :target: https://github.com/aioworkers/aioworkers-pg#readme
  :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/aioworkers-pg.svg
  :target: https://pypi.org/project/aioworkers-pg
  :alt: Python versions

.. image:: https://img.shields.io/pypi/dm/aioworkers-pg.svg
  :target: https://pypi.org/project/aioworkers-pg

.. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
  :alt: Hatch project
  :target: https://github.com/pypa/hatch


Asyncpg plugin for `aioworkers`.


Usage
-----

Connection
__________

Add this to aioworkers config.yaml:


.. code-block:: yaml

  db:
    cls: aioworkers_pg.base.Connector
    dsn: postgresql:///test

You can get access to postgres anywhere via context:

.. code-block:: python

  await context.db.execute("CREATE TABLE users(id serial PRIMARY KEY, name text)")
  await context.db.execute(users.insert().values(name="Bob"))


Connection additional
_____________________

.. code-block:: yaml

  db:
    cls: aioworkers_pg.base.Connector
    dsn: postgresql:///test
    pool:
      min_size: 1
      max_size: 100
    connection:  # optional
      init: mymodule.connection_init
      setup: mymodule.connection_setup
      class: mymodule.Connection


Storage
_______

.. code-block:: yaml

  storage:
    cls: aioworkers_pg.storage.RoStorage
    dsn: postgresql:///test
    table: mytable  # optional instead custom sql
    key: id
    get: SELECT * FROM mytable WHERE id = :id  # optional custom sql
    format: dict  # or row


Development
-----------

Check code:

.. code-block:: shell

    hatch run lint:all


Format code:

.. code-block:: shell

    hatch run lint:fmt


Run postgres:

.. code-block:: shell

  docker run --rm -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=test -d postgres


Run tests:

.. code-block:: shell

    hatch run pytest


Run tests with coverage:

.. code-block:: shell

    hatch run cov
