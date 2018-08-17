# !/usr/bin/python
"""The integration tests."""
# pylint: disable=protected-access
# because tests should access protected members
import os
import tempfile
import unittest

from plasoscaffolder.bll.services import sqlite_plugin_helper
from plasoscaffolder.bll.services import sqlite_plugin_path_helper
from plasoscaffolder.common import file_handler
from plasoscaffolder.dal import sqlite_query_execution
from plasoscaffolder.frontend.controller import sqlite_controller
from plasoscaffolder.model import sql_query_model
from tests.test_helper import output_handler_file
from tests.test_helper import path_helper


class GeneratingFilesTestCase(unittest.TestCase):
  """Class to do a integration test."""

  def testNormalGenerate(self):
    """Test a normal generation."""
    expected_path = os.path.join(os.path.dirname(__file__),
                                 'expected_files_twitterdb')
    plugin_name = 'the_plugin'
    database_suffix = 'db'
    test_file = os.path.join(path_helper.TestDatabasePath(), 'twitter_ios.db')
    with tempfile.TemporaryDirectory() as tmpdir:
      output_path = os.path.join(tmpdir, "temp")

      file_handler.FileHandler()._CreateFolder(output_path)

      output_console_path = os.path.join(output_path, 'prompts.txt')
      output_handler = output_handler_file.OutputHandlerFile(
          file_path=output_console_path,
          file_handler=file_handler.FileHandler(), confirm=True)

      sqlite_path_helper = sqlite_plugin_path_helper.SQLitePluginPathHelper(
          path=output_path, plugin_name=plugin_name,
          database_suffix=database_suffix)

      plugin_helper = sqlite_plugin_helper.SQLitePluginHelper()
      controller = sqlite_controller.SQLiteController(
          output_handler=output_handler, plugin_helper=plugin_helper)

      query_execution = sqlite_query_execution.SQLiteQueryExecution(test_file)
      query_execution.TryToConnect()

      query_first = 'select * from users'
      query_data_first = plugin_helper.RunSQLQuery(query_first, query_execution)
      data_first = plugin_helper.GetColumnsAndTimestampColumn(
          query_data_first.columns, ['createdDate', 'updatedAt'],
          query_data_first.data)
      query_data_first_timestamp = data_first[1]
      query_data_first_normal = data_first[0]
      query_data_first_normal[0].customize = True
      query_data_first_normal[1].customize = True
      query_data_first_normal[2].customize = True

      query_model_first = sql_query_model.SQLQueryModel(
          'select * from users', 'Users', query_data_first_normal,
          query_data_first_timestamp, True, len(query_data_first.data))

      query_second = 'select * from statuses'
      query_data_second = plugin_helper.RunSQLQuery(query_second,
                                                    query_execution)
      data_second = plugin_helper.GetColumnsAndTimestampColumn(
          query_data_second.columns, ['date', 'updatedAt'],
          query_data_second.data)
      query_data_second_timestamp = data_second[1]
      query_data_second_normal = data_second[0]

      query_model_second = sql_query_model.SQLQueryModel(
          'select * from users', 'Statuses', query_data_second_normal,
          query_data_second_timestamp, False, len(query_data_second.data))

      sql_query = [query_model_first, query_model_second]

      controller._path = output_path
      controller._name = plugin_name
      controller._testfile = test_file
      controller._sql_query = sql_query
      controller._plugin_helper = plugin_helper
      controller._output_handler = output_handler
      controller._query_execution = query_execution

      # Commenting out tests as part of project #1, issue #17.
      """
      controller.Generate(path_helper.TemplatePath(),
                          path_helper.YapfStyleFilePath())

      formatter_init = self._ReadFromFile(
          sqlite_path_helper.formatter_init_file_path)
      formatter = self._ReadFromFile(sqlite_path_helper.formatter_file_path)
      formatter_test = self._ReadFromFile(
          sqlite_path_helper.formatter_test_file_path)
      parser_init = self._ReadFromFile(
          sqlite_path_helper.parser_init_file_path)
      parser = self._ReadFromFile(sqlite_path_helper.parser_file_path)
      parser_test = self._ReadFromFile(sqlite_path_helper.parser_test_file_path)
      console_output = self._ReadFromFile(
          os.path.join(output_path, 'prompts.txt'))

      expected_formatter_init = self._ReadFromFile(os.path.join(
          expected_path, 'formatters_init.py'))
      expected_formatter = self._ReadFromFile(
          os.path.join(expected_path, 'formatters.py'))
      expected_formatter_test = self._ReadFromFile(os.path.join(
          expected_path, 'formatters_test.py'))
      expected_parser_init = self._ReadFromFile(
          os.path.join(expected_path, 'parsers_init.py'))
      expected_parser = self._ReadFromFile(
          os.path.join(expected_path, 'parsers.py'))
      expected_parser_test = self._ReadFromFile(
          os.path.join(expected_path, 'parsers_test.py'))
      expected_console_output = (
          'Do you want to Generate the files?create '
          '{0}create {1}create {2}create '
          '{3}copy {4}create {5}create {6}'.format(
              sqlite_path_helper.formatter_file_path,
              sqlite_path_helper.parser_file_path,
              sqlite_path_helper.formatter_test_file_path,
              sqlite_path_helper.parser_test_file_path,
              sqlite_path_helper.database_path,
              sqlite_path_helper.parser_init_file_path,
              sqlite_path_helper.formatter_init_file_path))

      self.assertEqual(formatter_init, expected_formatter_init)
      self.assertEqual(formatter, expected_formatter)
      self.assertEqual(formatter_test, expected_formatter_test)
      self.assertEqual(parser_init, expected_parser_init)
      self.assertEqual(parser, expected_parser)
      self.assertEqual(parser_test, expected_parser_test)
      self.assertEqual(console_output, expected_console_output)
      """

  def testNormalGenerateForAllTypes(self):
    """Test a normal generation."""
    expected_path = os.path.join(os.path.dirname(__file__),
                                 'expected_files_typesdb')
    plugin_name = 'the_plugin'
    database_suffix = 'db'
    test_file = os.path.join(path_helper.TestDatabasePath(),
                             'test_database_types.db')
    with tempfile.TemporaryDirectory() as tmpdir:
      output_path = os.path.join(tmpdir, "temp")

      file_handler.FileHandler()._CreateFolder(output_path)

      output_console_path = os.path.join(output_path, 'prompts.txt')
      output_handler = output_handler_file.OutputHandlerFile(
          file_path=output_console_path,
          file_handler=file_handler.FileHandler(), confirm=True)

      sqlite_path_helper = sqlite_plugin_path_helper.SQLitePluginPathHelper(
          path=output_path, plugin_name=plugin_name,
          database_suffix=database_suffix)

      plugin_helper = sqlite_plugin_helper.SQLitePluginHelper()
      controller = sqlite_controller.SQLiteController(
          output_handler=output_handler, plugin_helper=plugin_helper)

      query_execution = sqlite_query_execution.SQLiteQueryExecution(test_file)
      query_execution.TryToConnect()

      query_blob = 'select * from blobtypes'
      query_integer = 'select * from integertypes'
      query_numeric = 'select * from numerictypes'
      query_real = 'select * from realtypes'
      query_text = 'select * from texttypes'
      query_no_data = 'select * from nodata'

      query_data_blob = plugin_helper.RunSQLQuery(query_blob, query_execution)
      query_data_integer = plugin_helper.RunSQLQuery(query_integer,
                                                     query_execution)
      query_data_numeric = plugin_helper.RunSQLQuery(query_numeric,
                                                     query_execution)
      query_data_real = plugin_helper.RunSQLQuery(query_real, query_execution)
      query_data_text = plugin_helper.RunSQLQuery(query_text, query_execution)
      query_data_no_data = plugin_helper.RunSQLQuery(query_no_data,
                                                     query_execution)

      query_model_blob = sql_query_model.SQLQueryModel(
          query_blob, 'blobtypes', query_data_blob.columns, [], False, 0)
      query_model_integer = sql_query_model.SQLQueryModel(
          query_integer, 'integertypes', query_data_integer.columns, [], False,
          0)
      query_model_numeric = sql_query_model.SQLQueryModel(
          query_numeric, 'numerictypes', query_data_numeric.columns, [], False,
          0)
      query_model_real = sql_query_model.SQLQueryModel(
          query_real, 'realtypes', query_data_real.columns, [], False, 0)
      query_model_text = sql_query_model.SQLQueryModel(
          query_text, 'texttypes', query_data_text.columns, [], False, 0)
      query_model_no_data = sql_query_model.SQLQueryModel(
          query_no_data, 'nodata', query_data_no_data.columns, [], False, 0)

      sql_query = [query_model_blob, query_model_integer, query_model_numeric,
                   query_model_real, query_model_text, query_model_no_data]

      controller._path = output_path
      controller._name = plugin_name
      controller._testfile = test_file
      controller._sql_query = sql_query
      controller._plugin_helper = plugin_helper
      controller._output_handler = output_handler
      controller._query_execution = query_execution

      controller.Generate(path_helper.TemplatePath(),
                          path_helper.YapfStyleFilePath())

      formatter_init = self._ReadFromFile(
          sqlite_path_helper.formatter_init_file_path)
      formatter = self._ReadFromFile(sqlite_path_helper.formatter_file_path)
      formatter_test = self._ReadFromFile(
          sqlite_path_helper.formatter_test_file_path)
      parser_init = self._ReadFromFile(
          sqlite_path_helper.parser_init_file_path)
      parser = self._ReadFromFile(sqlite_path_helper.parser_file_path)
      parser_test = self._ReadFromFile(sqlite_path_helper.parser_test_file_path)
      console_output = self._ReadFromFile(
          os.path.join(output_path, 'prompts.txt'))

      expected_formatter_init = self._ReadFromFile(os.path.join(
          expected_path, 'formatters_init.py'))
      expected_formatter = self._ReadFromFile(
          os.path.join(expected_path, 'formatters.py'))
      expected_formatter_test = self._ReadFromFile(os.path.join(
          expected_path, 'formatters_test.py'))
      expected_parser_init = self._ReadFromFile(
          os.path.join(expected_path, 'parsers_init.py'))
      expected_parser = self._ReadFromFile(
          os.path.join(expected_path, 'parsers.py'))
      expected_parser_test = self._ReadFromFile(
          os.path.join(expected_path, 'parsers_test.py'))
      expected_console_output = (
          'Do you want to Generate the files?create '
          '{0}create {1}create {2}create '
          '{3}copy {4}create {5}create {6}'.format(
              sqlite_path_helper.formatter_file_path,
              sqlite_path_helper.parser_file_path,
              sqlite_path_helper.formatter_test_file_path,
              sqlite_path_helper.parser_test_file_path,
              sqlite_path_helper.database_path,
              sqlite_path_helper.parser_init_file_path,
              sqlite_path_helper.formatter_init_file_path))

      self.assertEqual(formatter_init, expected_formatter_init)
      self.assertEqual(formatter, expected_formatter)
      self.assertEqual(formatter_test, expected_formatter_test)
      self.assertEqual(parser_init, expected_parser_init)
      # Commenting out tests as part of project #1, issue #17.
      #self.assertEqual(parser, expected_parser)
      self.assertEqual(parser_test, expected_parser_test)
      self.assertEqual(console_output, expected_console_output)

  def _ReadFromFile(self, path: str):
    """read from file helper"""
    with open(path, 'r') as f:
      return f.read()


if __name__ == '__main__':
  unittest.main()
