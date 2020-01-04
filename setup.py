#!/usr/bin/env python

import pathlib

from setuptools import find_packages, setup


package = 'aioworkers_pg'
version = __import__(package).__version__
readme = pathlib.Path('README.rst').read_text()


setup(
    name='aioworkers-pg',
    version=version,
    description='Module for working with PostgreSQL via asyncpg',
    long_description=readme,
    author='Alexander Bogushov',
    author_email='abogushov@gmail.com',
    url='https://github.com/aioworkers/aioworkers-pg',
    packages=find_packages(include=[package, package + '.*']),
    include_package_data=True,
    install_requires=[
        'aioworkers>=0.15',
        'asyncpg',
    ],
    extras_require={'sa': ['sqlalchemy', 'asyncpgsa']},
    license='Apache Software License 2.0',
    keywords='aioworkers asyncpg',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
