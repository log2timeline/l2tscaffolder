# -*- coding: utf-8 -*-
"""Tests for the plugin plugin."""
import unittest

from plaso.lib import eventdata
from plaso.lib import timelib
from plaso.parsers.sqlite_plugins import the_plugin

from tests import test_lib as shared_test_lib
from tests.parsers.sqlite_plugins import test_lib


class ThePluginTest(test_lib.SQLitePluginTestCase):
  """Tests for the plugin database plugin."""

  @shared_test_lib.skipUnlessHasTestFile([u'the_plugin.db'])
  def testProcess(self):
    """Test the Process function on a The Plugin file."""
    plugin_object = the_plugin.ThePluginPlugin()
    storage_writer = self._ParseDatabaseFileWithPlugin([u'the_plugin.db'],
                                                       plugin_object)

    # We should have 0 events in total.

    self.assertEqual(0, len(storage_writer.events))


if __name__ == '__main__':
  unittest.main()
