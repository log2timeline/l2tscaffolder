# -*- coding: utf-8 -*-
"""Parser for testing database.

SQLite database path: test_data/test_sqlite.db
SQLite database Name: test_sqlite.db
"""

from dfdatetime import posix_time as dfdatetime_posix_time

from plaso.containers import time_events
from plaso.lib import eventdata
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface


class TestingStrangeEventData(events.EventData):
  """testing strange event data.

  Attributes:
    name: <ADD DESCRIPTION HERE>
    address: <ADD DESCRIPTION HERE>
    ssn: <ADD DESCRIPTION HERE>

  """

  DATA_TYPE = u'testing:strange'

  def __init__(self):
    """Initializes event data."""
    super(TestingStrangeEventData, self).__init__(data_type=self.DATA_TYPE)
    self.address = None
    self.name = None
    self.ssn = None


class TestingFoobarEventData(events.EventData):
  """testing foobar event data.

  Attributes:
    foo: <ADD DESCRIPTION HERE>
    bar: <ADD DESCRIPTION HERE>

  """

  DATA_TYPE = u'testing:foobar'

  def __init__(self):
    """Initializes event data."""
    super(TestingFoobarEventData, self).__init__(data_type=self.DATA_TYPE)
    self.bar = None
    self.foo = None


class TestingPlugin(interface.SQLitePlugin):
  """Parser for Testing"""

  NAME = u'testing'
  DESCRIPTION = u'Parser for Testing'

  QUERIES = [
      ((u'SELECT name, address, ssn FROM strange)'), u'ParseStrangeRow'), ((
          u'SELECT f1.foo, f2.bar AS Bar FROM foobar_one AS f1, foobar_two'
          u'as f2 WHERE f1.id = f2.id)'), u'ParseFoobarRow')
  ]

  REQUIRED_TABLES = frozenset([u'foobar_one', u'foobar_two', u'strange_table'])

  SCHEMAS = [{
      'foobar_one': ('CREATE TABLE foobar_one(id INT, foo VARCHAR)'),
      'foobar_two': ('CREATE TABLE foobar_two(id INT, bar VARCHAR)'),
      'strange_table': (
          'CREATE TABLE strange_table(id INT, id2 INT, id3 INT, secret INT,'
          'name VARCHAR, address VARCHAR, ssn INT)')
  }]

  def ParseStrangeRow(self, parser_mediator, query, row, **unused_kwargs):
    """Parses a row from the database.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfvfs.
      query (str): query that created the row.
      row (sqlite3.Row): row resulting from query.
    """
    # Note that pysqlite does not accept a Unicode string in row['string'] and
    # will raise "IndexError: Index must be int or string".

    event_data = TestingStrangeEventData()
    event_data.address = row['address']
    event_data.name = row['name']
    event_data.ssn = row['ssn']

  def ParseFoobarRow(self, parser_mediator, query, row, **unused_kwargs):
    """Parses a row from the database.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfvfs.
      query (str): query that created the row.
      row (sqlite3.Row): row resulting from query.
    """
    # Note that pysqlite does not accept a Unicode string in row['string'] and
    # will raise "IndexError: Index must be int or string".

    event_data = TestingFoobarEventData()
    event_data.bar = row['bar']
    event_data.foo = row['foo']


sqlite.SQLiteParser.RegisterPlugin(TestingPlugin)
