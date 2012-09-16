# -*- coding: utf-8 -*-

from nose.tools import *
import fixer

import data


def assert_sequence_contains(actual, expected):
    diff = set(expected).difference(set(actual))
    if diff:
        raise AssertionError(u'{0} are missing from {1}'.format(list(diff), expected))


def setup():
    # data.connect('postgresql://robc@127.0.0.1/fixture_testing')
    data.connect('postgresql://ubuntu@127.0.0.1/circle_test')
    data.Base.metadata.drop_all()


def teardown():
    data.Base.metadata.drop_all()


def test_init_db():
    """The loader correctly initialises the db given a bound Metadata instance
    """
    metadata = data.Base.metadata
    loader = fixer.Loader(data.Session, metadata)

    existing_tables = metadata.bind.table_names()
    expected_tables = metadata.tables.keys()

    ## DB has no tables defined in Metadata
    unexpected_existing_tables = set(existing_tables).intersection(set(expected_tables))
    assert_false(unexpected_existing_tables)

    loader.init_db(drop=True)

    ## DB now has all tables defined in Metadata
    existing_tables = metadata.bind.table_names()
    assert_sequence_contains(existing_tables, expected_tables)
