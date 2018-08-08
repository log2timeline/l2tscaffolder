# -*- coding: utf-8 -*-
"""Parser for test database.

SQLite database path:
# TODO: add database path
SQLite database Name: test.db
"""

from dfdatetime import posix_time as dfdatetime_posix_time

from plaso.containers import time_events
from plaso.lib import eventdata
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface


class TestUsersstatusesEventData(events.EventData):
  """test usersstatuses event data.

  TODO: add type and description of attributes
  Attributes:
    user_id (int): TODO
  """

  DATA_TYPE = u'test:'

  def __init__(self):
    """Initializes event data."""
    super(TestUsersstatusesEventData, self).__init__(data_type=self.DATA_TYPE)
    self.user_id = None


class TestPlugin(interface.SQLitePlugin):
  """Parser for Test"""

  NAME = u'test'
  DESCRIPTION = u'Parser for Test'

  QUERIES = [((
      u'select users.id as user_id , users.updatedAt as updatedAt,'
      u'createdDate from users join statuses)'), u'ParseUsersstatusesRow')]

  REQUIRED_TABLES = frozenset([
      u'Lists', u'ListsShadow', u'MyRetweets', u'Statuses', u'StatusesShadow',
      u'Users', u'UsersShadow'
  ])

  def ParseUsersstatusesRow(
      self, parser_mediator, row, query=None, **unused_kwargs):
    """Parses a contact row from the database.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfvfs.
      row (sqlite3.Row): row resulting from Query.
      Query (Optional[str]): Query.
    """
    # Note that pysqlite does not accept a Unicode string in row['string'] and
    # will raise "IndexError: Index must be int or string".

    event_data = TestEventData()
    event_data.user_id = row['user_id']

    timestamp = row['createdDate']
    if timestamp:
      # Convert the floating point value to an integer.
      timestamp = int(timestamp)
      date_time = dfdatetime_posix_time.PosixTime(timestamp=timestamp)
      # TODO: Add correct time field for None value.  Example: eventdata.EventTimestamp.UPDATE_TIME
      event = time_events.DateTimeValuesEvent(date_time, None)
      parser_mediator.ProduceEventWithEventData(event, event_data)

    timestamp = row['updatedAt']
    if timestamp:
      # Convert the floating point value to an integer.
      timestamp = int(timestamp)
      date_time = dfdatetime_posix_time.PosixTime(timestamp=timestamp)
      # TODO: Add correct time field for None value.  Example: eventdata.EventTimestamp.UPDATE_TIME
      event = time_events.DateTimeValuesEvent(date_time, None)
      parser_mediator.ProduceEventWithEventData(event, event_data)


sqlite.SQLiteParser.RegisterPlugin(TestPlugin)
