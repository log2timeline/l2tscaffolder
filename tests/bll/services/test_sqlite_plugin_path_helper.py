# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test class"""
import os
import unittest

from plasoscaffolder.bll.services.sqlite_plugin_path_helper import \
  SQLitePluginPathHelper


class SQLitePluginPathHelperTest(unittest.TestCase):
  """  Class representing a test case testing the SQLite plugin helper"""

  def setUp(self):
    path = "temp"
    plugin_name = "plugin_test"
    self.helper = SQLitePluginPathHelper(path, plugin_name, "db")
    plugin_file = plugin_name + ".py"
    self.formatter = (path + os.sep + "plaso" + os.sep + "formatters" + os.sep
                      + plugin_file)
    self.formatter_test = (path + os.sep + "tests" + os.sep + "formatters" +
                           os.sep + plugin_file)

    self.parser = (path + os.sep + "plaso" + os.sep + "parsers" + os.sep +
                   "sqlite_plugins" + os.sep + plugin_file)
    self.parser_test = (path + os.sep + "tests" + os.sep + "parsers" + os.sep +
                        "sqlite_plugins" + os.sep + plugin_file)
    self.database = path + os.sep + "test_data" + os.sep + plugin_name + ".db"
    self.parser_init = (path + os.sep + "plaso" + os.sep + "parsers" + os.sep +
                        "sqlite_plugins" + os.sep + "__init__.py")
    self.formatter_init = (path + os.sep + "plaso" + os.sep + "formatters" +
                           os.sep + "__init__.py")

  def testFormatterFilePath(self):
    """Tests the creation of the path for the formatter file."""
    actual = self.helper.formatter_file_path
    self.assertEqual(actual, self.formatter)

  def testFormatterTestFilePath(self):
    """Tests the creation of the path for the formatter test file."""
    actual = self.helper.formatter_test_file_path
    self.assertEqual(self.formatter_test, actual)

  def testParserFilePath(self):
    """Tests the creation of the path for the parser file."""
    actual = self.helper.parser_file_path
    self.assertEqual(self.parser, actual)

  def test_parser_test_file(self):
    """Tests the creation of the path for the parser test file."""
    actual = self.helper.parser_test_file_path
    self.assertEqual(self.parser_test, actual)

  def test_database_file(self):
    """Tests the creation of the path for the database file."""
    actual = self.helper.database_path
    self.assertEqual(self.database, actual)

  def test_formatter_init_file(self):
    """Tests the creation of the path for the formatter init file."""
    actual = self.helper.formatter_init_file_path
    self.assertEqual(self.formatter_init, actual)

  def test_parser_init__file(self):
    """Tests the creation of the path for the parser init file."""
    actual = self.helper.parser_init_file_path
    self.assertEqual(self.parser_init, actual)


if __name__ == '__main__':
  unittest.main()
