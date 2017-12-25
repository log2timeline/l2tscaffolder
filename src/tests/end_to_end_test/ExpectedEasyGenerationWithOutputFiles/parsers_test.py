# -*- coding: utf-8 -*-
"""Tests for test plugin."""
import unittest

from plaso.lib import eventdata
from plaso.lib import timelib
from plaso.parsers.sqlite_plugins import test

from tests import test_lib as shared_test_lib
from tests.parsers.sqlite_plugins import test_lib


class TestTest(test_lib.SQLitePluginTestCase):
  """Tests for test database plugin."""

  @shared_test_lib.skipUnlessHasTestFile([u'test.db'])
  def testProcess(self):
    """Test the Process function on a Test file."""
    plugin_object = test.TestPlugin()
    storage_writer = self._ParseDatabaseFileWithPlugin([u'test.db'],
                                                       plugin_object)

    # We should have 25 events in total.
    # - 25 Users createdDate events.

    self.assertEqual(25, len(storage_writer.events))

    # Test the first users createdDate event.
    guessed_event = [
        e for e in storage_writer.events
        if e.id == 5402612 and e.name == u'BBC Breaking News'
    ][0]
    position = storage_writer.index(guessed_event)
    test_event = storage_writer.events[position]

    # TODO add expected formatted timestamp for timestamp in database: 1177252957.0
    expected_timestamp = timelib.Timestamp.CopyFromString(u'TODO')
    self.assertEqual(test_event.timestamp, expected_timestamp)

    self.assertEqual(
        test_event.timestamp_desc, eventdata.EventTimestamp.CREATION_TIME)
    self.assertEqual(test_event.id, 5402612)
    self.assertEqual(test_event.name, u'BBC Breaking News')

    expected_message = (u'Id: 5402612 Name: BBC Breaking News')
    expected_message_short = (u'Id: 5402612 Name: BBC Breaking News...')

    self._TestGetMessageStrings(
        test_event, expected_message, expected_message_short)


if __name__ == '__main__':
  unittest.main()
