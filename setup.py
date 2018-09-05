#!/usr/bin/env python

from setuptools import setup, find_packages

version = __import__('aioworkers_pg').__version__

requirements = [
    'aioworkers>=0.8.0',
    'asyncpg',
]

test_requirements = [
    'pytest',
    'pytest-runner',
    'pytest-aiohttp',
    'pytest-flake8',
    'flake8-isort',
]

setup(
    name='aioworkers-pg',
    version=version,
    description='Module for working with Postgres SQL via asyncpg',
    author='Alexander Bogushov',
    author_email='abogushov@gmail.com',
    url='https://github.com/aioworkers/aioworkers-pg',
    packages=[i for i in find_packages() if i.startswith('aioworkers_pg')],
    include_package_data=True,
    install_requires=requirements,
    license='Apache Software License 2.0',
    keywords='aioworkers asyncpg',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
