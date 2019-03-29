aioworkers-pg
================

.. image:: https://travis-ci.org/aioworkers/aioworkers-pg.svg?branch=master
  :target: https://travis-ci.org/aioworkers/aioworkers-pg

.. image:: https://img.shields.io/pypi/pyversions/aioworkers-pg.svg
  :target: https://pypi.python.org/pypi/aioworkers-pg
  :alt: Python versions

.. image:: https://img.shields.io/pypi/v/aioworkers-pg.svg
  :target: https://pypi.python.org/pypi/aioworkers-pg


Asyncpg plugin for `aioworkers`.


Usage
-----

Add this to aioworkers config.yaml:

.. code-block:: yaml

    db:
        cls: aioworkers_pg.base.Connector
        dsn: postgresql:///test

You can get access to postgres anywhere via context:

.. code-block:: python

    await context.db.execute('CREATE TABLE users(id serial PRIMARY KEY, name text)')
    await context.db.execute(users.insert().values(name='Bob'))


Storage
~~~~~~~

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

Install dev requirements:


.. code-block:: shell

    pipenv install --dev --skip-lock


Run tests:

.. code-block:: shell

    pytest