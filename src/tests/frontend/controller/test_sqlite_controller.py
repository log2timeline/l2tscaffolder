# !/usr/bin/python
# -*- coding: utf-8 -*-
"""test class"""
# pylint: disable=protected-access
# because tests should access protected members
import os
import pathlib
import tempfile
import unittest
from unittest import mock

from plasoscaffolder.bll.services import sqlite_plugin_helper
from plasoscaffolder.common import file_handler
from plasoscaffolder.dal import sql_query_data
from plasoscaffolder.frontend.controller import sqlite_controller
from plasoscaffolder.model import (sql_query_column_model,
                                   sql_query_column_model_data, sql_query_model)
from tests.fake import fake_sqlite_plugin_helper
from tests.fake import fake_sqlite_query_execution
from tests.test_helper import output_handler_file
from tests.test_helper import path_helper


class SQLiteControllerTest(unittest.TestCase):
  """Tests the SQLite controller"""

  def testPluginNameIfExisting(self):
    """test method after getting the plugin Name from the user if the plugin
    Name already exists"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_info='the_plugin',
          prompt_error='the_plugin', )
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          plugin_exists=True, change_bool_after_every_call_plugin_exists=True,
          valid_name=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      actualName = 'the_plugin'
      controller._path = 'somepath'
      actual = controller.PluginName(None, None, actualName)
      expected = 'Plugin exists. Choose new Name'
      actual_prompt = self._ReadFromFile(path)
      self.assertEqual(expected, actual_prompt)
      self.assertEqual(actualName, actual)

  def testPluginNameIfNotExisting(self):
    """test method after getting tplugin Name from the user if the plugin
    Name is new"""

    output_handler = output_handler_file.OutputHandlerFile(
        'somefile', file_handler.FileHandler())
    plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
        plugin_exists=False)
    controller = sqlite_controller.SQLiteController(output_handler,
                                                    plugin_helper)
    actualName = 'the_plugin'
    controller._path = 'somepath'
    actual = controller.PluginName(None, None, actualName)
    self.assertEqual(actualName, controller._name)
    self.assertEqual(actual, actualName)

  def testSourcePathIfExisting(self):
    """test method after getting the source path from the user"""

    output_handler = output_handler_file.OutputHandlerFile(
        'somefile', file_handler.FileHandler())
    plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
        folder_exists=True)
    controller = sqlite_controller.SQLiteController(output_handler,
                                                    plugin_helper)
    actualPath = 'testpath'
    actual = controller.SourcePath(None, None, actualPath)
    self.assertEqual(actualPath, controller._path)
    self.assertEqual(actual, actualPath)

  def testCreateSQLQueryModelWithUserInputNoError(self):
    """test method CreateEventModelWithUserInput"""

    fake_execution = fake_sqlite_query_execution.SQLQueryExecution(
        sql_query_data.SQLQueryData(has_error=False)
    )
    sql_query = 'SELECT createdDate FROM Users ORDER BY createdDate'
    name = 'Contact'
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(),
          confirm=True, confirm_amount_same=2, prompt_info=name)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          folder_exists=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      controller.GetTimestamps = mock.MagicMock(return_value=([], []))
      actual = controller._CreateSQLQueryModelWithUserInput(sql_query, False,
                                                            fake_execution)
      prompt_output_actual = self._ReadFromFile(path)
      prompt_output_expected = (
          'The SQL query was ok.'
          'Do you want to name the query parse row:  ?'
          'Does the event  need customizing?'
          'Enter columns that are customizable [columnName,aliasName...] '
          'or [abort]'
          'Added: Failed: Contact'
          'Do you want to add more columns that are customizable?')

      expected = sql_query_model.SQLQueryModel(
          sql_query, name, [], [], False, 0)
      self.assertEqual(actual.name, '')
      self.assertEqual(expected.query, actual.query)
      self.assertEqual(prompt_output_expected, prompt_output_actual)

  def testCreateSQLQueryModelWithUserInputWithExamplesAndFourDataExamples(self):
    """test method CreateEventModelWithUserInput with examples"""

    fake_execution = fake_sqlite_query_execution.SQLQueryExecution(
        sql_query_data.SQLQueryData(
            has_error=False, data=['first', 'second', 'third', 'fourth'],
            columns=[type('columns', (object,), {'sql_column': 'id'}),
                     type('columns', (object,), {'sql_column': 'name'})])
    )
    sql_query = 'SELECT id from Users'
    name = 'Contact'
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(),
          confirm=True, confirm_amount_same=2, prompt_info=name)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          folder_exists=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      controller.GetTimestamps = mock.MagicMock(return_value=([], []))
      actual = controller._CreateSQLQueryModelWithUserInput(sql_query, True,
                                                            fake_execution)
      prompt_output_actual = self._ReadFromFile(path)
      prompt_output_expected = ('Your query output could look like this.'
                                '[\'id\', \'name\']'
                                'first'
                                'second'
                                'third'
                                'Do you want to add this query?'
                                'Do you want to name the query parse row:  ?'
                                'Does the event  need customizing?')

      expected = sql_query_model.SQLQueryModel(sql_query, name, [], [], False,
                                               0)

      self.assertEqual(actual.name, '')
      self.assertEqual(expected.query, actual.query)
      self.assertEqual(prompt_output_expected, prompt_output_actual)

  def testCreateSQLQueryModelWithUserInputWithExamplesAndTwoDataExamples(self):
    """test method CreateEventModelWithUserInput with examples"""

    fake_execution = fake_sqlite_query_execution.SQLQueryExecution(
        sql_query_data.SQLQueryData(
            has_error=False, data=['first', 'second'],
            columns=[type('columns', (object,), {'sql_column': 'id'}),
                     type('columns', (object,), {'sql_column': 'name'})])
    )
    sql_query = 'SELECT id from Users'
    name = 'Contact'
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(),
          confirm=True, confirm_amount_same=2, prompt_info=name)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          folder_exists=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      controller.GetTimestamps = mock.MagicMock(return_value=([], []))
      actual = controller._CreateSQLQueryModelWithUserInput(sql_query, True,
                                                            fake_execution)
      prompt_output_actual = self._ReadFromFile(path)
      prompt_output_expected = ('Your query output could look like this.'
                                '[\'id\', \'name\']'
                                'first'
                                'second'
                                'Do you want to add this query?'
                                'Do you want to name the query parse row:  ?'
                                'Does the event  need customizing?')

      expected = sql_query_model.SQLQueryModel(
          sql_query, name, [], [], False, 0)

      self.assertEqual(actual.name, '')
      self.assertEqual(expected.query, actual.query)
      self.assertEqual(prompt_output_expected, prompt_output_actual)

  def testCreateSQLQueryModelWithUserInputWithExamplesAndOneDataExamples(self):
    """test method CreateEventModelWithUserInput with examples"""

    fake_execution = fake_sqlite_query_execution.SQLQueryExecution(
        sql_query_data.SQLQueryData(
            has_error=False, data=['first'],
            columns=[type('columns', (object,), {'sql_column': 'id'}),
                     type('columns', (object,), {'sql_column': 'name'})])
    )
    sql_query = 'SELECT id from Users'
    name = 'Contact'
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(),
          confirm=True, confirm_amount_same=2, prompt_info=name)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          folder_exists=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      controller.GetTimestamps = mock.MagicMock(return_value=([], []))
      actual = controller._CreateSQLQueryModelWithUserInput(sql_query, True,
                                                            fake_execution)
      prompt_output_actual = self._ReadFromFile(path)
      prompt_output_expected = ('Your query output could look like this.'
                                '[\'id\', \'name\']'
                                'first'
                                'Do you want to add this query?'
                                'Do you want to name the query parse row:  ?'
                                'Does the event  need customizing?')

      expected = sql_query_model.SQLQueryModel(sql_query, name, [], [], False,
                                               0)

      self.assertEqual(actual.name, '')
      self.assertEqual(expected.query, actual.query)
      self.assertEqual(prompt_output_expected, prompt_output_actual)

  def testCreateSQLQueryModelWithUserInputExamplesNewRowNameValidationError(
      self):
    """test method CreateEventModelWithUserInput with examples"""

    fake_execution = fake_sqlite_query_execution.SQLQueryExecution(
        sql_query_data.SQLQueryData(
            has_error=False, data=['first'],
            columns=[type('columns', (object,), {'sql_column': 'id'}),
                     type('columns', (object,), {'sql_column': 'name'})])
    )
    sql_query = 'SELECT id from Users'
    name = 'Contact'
    name2 = 'TheCorrectContanctName'

    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(),
          confirm=True, confirm_amount_same=1, prompt_info=name,
          prompt_error=name2)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          folder_exists=True, valid_row_name=False,
          change_bool_after_every_call_valid_row_name=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      controller.GetTimestamps = mock.MagicMock(return_value=([], []))
      actual = controller._CreateSQLQueryModelWithUserInput(sql_query, True,
                                                            fake_execution)
      prompt_output_actual = self._ReadFromFile(path)
      prompt_output_expected = (
          'Your query output could look like this.'
          '[\'id\', \'name\']'
          'first'
          'Do you want to add this query?'
          'Do you want to name the query parse row:  ?'
          'What row does the SQL Query parse?'
          'Row name is not in a valid format. Choose new Name [RowName...]'
          'Does the event TheCorrectContanctName need customizing?')
      expected = sql_query_model.SQLQueryModel(sql_query, name, [], [], False,
                                               0)

      self.assertEqual(actual.name, name2)
      self.assertEqual(expected.query, actual.query)
      self.assertEqual(prompt_output_expected, prompt_output_actual)

  def testCreateSQLQueryModelWithUserInputWithExamplesAndNoDataFromQuery(self):
    """test method CreateEventModelWithUserInput with examples"""

    fake_execution = fake_sqlite_query_execution.SQLQueryExecution(
        sql_query_data.SQLQueryData(has_error=False, data=[])
    )
    sql_query = 'SELECT id from Users'
    name = 'Contact'
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(),
          confirm=True, confirm_amount_same=2, prompt_info=name)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          folder_exists=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      controller.GetTimestamps = mock.MagicMock(return_value=([], []))
      actual = controller._CreateSQLQueryModelWithUserInput(sql_query, True,
                                                            fake_execution)
      prompt_output_actual = self._ReadFromFile(path)
      prompt_output_expected = ('Your query does not return anything.'
                                'Do you want to add this query?'
                                'Do you want to name the query parse row:  ?'
                                'Does the event  need customizing?')

      expected = sql_query_model.SQLQueryModel(sql_query, name, [], [], False,
                                               0)

      self.assertEqual(actual.name, '')
      self.assertEqual(expected.query, actual.query)
      self.assertEqual(prompt_output_expected, prompt_output_actual)

  def testCreateSQLQueryModelWithUserInputWithError(self):
    """test method CreateEventModelWithUserInput"""
    error_message = "Some Error..."
    fake_execution = fake_sqlite_query_execution.SQLQueryExecution(
        sql_query_data.SQLQueryData(has_error=True,
                                    error_message=error_message)
    )
    sql_query = 'SELECT createdDate FROM Users ORDER BY createdDate'
    name = 'Contact'
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_info=name)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          folder_exists=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      actual = controller._CreateSQLQueryModelWithUserInput(sql_query, False,
                                                            fake_execution)
      self.assertIsNone(actual)

  def testSqlQuery(self):
    """test method after getting the source path from the user"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), confirm=False)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper()
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)

      controller._CreateSQLQueryModelWithUserInput = mock.MagicMock(
          return_value=sql_query_data.SQLQueryData(
              data='test', has_error=False, error_message=None))

      actual = controller.SQLQuery(None, None, True)

      prompt_output_actual = self._ReadFromFile(path)

      prompt_output_expected = ('Please write your SQL script for the plugin'
                                'Do you want to add another Query?')

      self.assertEqual(len(actual), 1)
      self.assertEqual(actual[0].data, 'test')
      self.assertEqual(actual[0].has_error, False)
      self.assertEqual(actual[0].error_message, None)
      self.assertEqual(prompt_output_actual, prompt_output_expected)

  def testSqlQueryWithAbort(self):
    """test method after getting the source path from the user using abort"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_info='abort', confirm=True,
          confirm_amount_same=2)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper()
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)

      controller._CreateSQLQueryModelWithUserInput = mock.MagicMock(
          return_value=sql_query_model.SQLQueryModel(
              'query', 'name', None, None, True, 0))

      actual = controller.SQLQuery(None, None, True)

      prompt_output_actual = self._ReadFromFile(path)
      prompt_output_expected = (
          'Please write your SQL script for the plugin'
          'Do you want to add another Query?'
          'Please write your SQL script for the plugin [\'abort\' to continue]')

      self.assertEqual(len(actual), 1)
      self.assertEqual(actual[0].query, 'query')
      self.assertEqual(prompt_output_actual, prompt_output_expected)

  def testSqlQueryMultiple(self):
    """test method after getting the source path from the user"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), confirm=True, confirm_amount_same=2)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper()
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)

      controller._CreateSQLQueryModelWithUserInput = mock.MagicMock(
          return_value=sql_query_data.SQLQueryData(
              data='test', has_error=False, error_message=None))

      actual = controller.SQLQuery(None, None, True)

      prompt_output_expected = (
          'Please write your SQL script for the plugin'
          'Do you want to add another Query?'
          'Please write your SQL script for the plugin [\'abort\' to continue]'
          'Do you want to add another Query?'
          'Please write your SQL script for the plugin [\'abort\' to continue]'
          'Do you want to add another Query?'
      )
      prompt_output_actual = self._ReadFromFile(path)

    self.assertEqual(len(actual), 3)
    self.assertEqual(actual[0].data, 'test')
    self.assertEqual(actual[0].has_error, False)
    self.assertEqual(actual[0].error_message, None)
    self.assertEqual(actual[1].data, 'test')
    self.assertEqual(actual[1].has_error, False)
    self.assertEqual(actual[1].error_message, None)
    self.assertEqual(actual[2].data, 'test')
    self.assertEqual(actual[2].has_error, False)
    self.assertEqual(actual[2].error_message, None)

    self.assertEqual(prompt_output_actual, prompt_output_expected)

  def testSourcePathIfNotExisting(self):
    """test method after getting the source path from the user"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_error='the source path')
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          folder_exists=False, change_bool_after_every_call_folder_exists=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      actualPath = 'testpath'
      source_path = controller.SourcePath(None, None, actualPath)
      expected = 'Folder does not exists. Enter correct one'
      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(source_path, 'the source path')

  def testTestPathIfExisting(self):
    """test method after getting the source path from the user"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler())
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          file_exists=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      actualPath = os.path.join(path_helper.TestDatabasePath(),
                                'twitter_ios.db')
      valid_path = controller.TestPath(None, None, actualPath)

      actual_output = self._ReadFromFile(path)
      self.assertEqual(actualPath, controller._testfile)
      self.assertEqual('', actual_output)
      self.assertEqual(valid_path, actualPath)

  def testTestPathIfExistingAndNoDatabaseFile(self):
    """test method after getting the source path from the user"""

    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      error_file = os.path.join(path_helper.TestDatabasePath(),
                                'twitter_ios_error.db')
      correct_file = os.path.join(path_helper.TestDatabasePath(),
                                  'twitter_ios.db')

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_error=correct_file)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          file_exists=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)

      valid_path = controller.TestPath(None, None, error_file)

      actual_output = self._ReadFromFile(path)
      expected_output = 'Unable to open the database file. Choose another.'
      self.assertEqual(correct_file, controller._testfile)
      self.assertEqual(expected_output, actual_output)
      self.assertEqual(valid_path, correct_file)

  def testTestPathIfNotExisting(self):
    """test method after getting the source path from the user"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()
      wrongPath = os.path.join(tmpdir, 'testpath')
      validPath = os.path.join(tmpdir, 'testpathvalid')

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_error=validPath)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          file_exists=False, change_bool_after_every_call_file_exists=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      actual_path = controller.TestPath(None, None, wrongPath)
      expected = 'File does not exists. Choose another.'
      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(validPath, actual_path)
      # close connection so the temp file can be deleted before the program
      #   circle is finished
      controller._query_execution._connection.close()

  def testValidatePluginNameIfOk(self):
    """test the validate plugin Name method if ok"""
    plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
        valid_name=True)
    controller = sqlite_controller.SQLiteController(None, plugin_helper)
    valid_plugin = controller._ValidatePluginName("the_plugin")
    self.assertTrue(valid_plugin)

  def testValidatePluginNameIfNotOk(self):
    """test the validate plugin Name method if not ok"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_error='valid_name')
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          valid_name=False, change_bool_after_every_call_valid_name=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      valid = controller._ValidatePluginName("the_wrong_plugin_")
      expected = ('Plugin is not in a valid format. Choose new Name ['
                  'plugin_name_...]')
      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(valid, 'valid_name')

  def testValidateRowNameNameIfOk(self):
    """test the validate row name method if ok"""
    plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
        valid_name=True)
    controller = sqlite_controller.SQLiteController(None, plugin_helper)
    valid = controller._ValidateRowName("TheRowName")
    self.assertEqual(valid, 'TheRowName')

  def testValidateRowNameIfNotOk(self):
    """test the validate row name method if not ok"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_error='TheValidRowName')
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          valid_row_name=False,
          change_bool_after_every_call_valid_row_name=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      valid = controller._ValidateRowName("theWrongName")
      expected = ('Row name is not in a valid format. Choose new Name ['
                  'RowName...]')
      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(valid, 'TheValidRowName')

  def testValidateTimestampStringIfOk(self):
    """test the validate timestamp string method if ok"""
    plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
        valid_name=True)
    controller = sqlite_controller.SQLiteController(None, plugin_helper)
    valid = controller._ValidateTimestampString("this,that,bla")
    self.assertEqual(valid, 'this,that,bla')

  def testValidateTimestampStringIfNotOk(self):
    """test the validate timestamp string method if not ok"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_error='this,that,bla')
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          valid_comma_separated_string=False,
          change_bool_after_every_call_valid_comma_separated_string=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      valid = controller._ValidateTimestampString("this, that,bla")
      expected = (
          'Timestamps are not in valid format. Reenter them correctly [name,'
          'name...]')
      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(valid, 'this,that,bla')

  def testValidateColumnStringIfOk(self):
    """test the validate column string method if ok"""
    plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
        valid_name=True)
    controller = sqlite_controller.SQLiteController(None, plugin_helper)
    valid = controller._ValidateColumnString("this,that,bla")
    self.assertEqual(valid, 'this,that,bla')

  def testValidateColumnStringIfNotOk(self):
    """test the validate column string method if not ok"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_error='this,that,bla')
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          valid_comma_separated_string=False,
          change_bool_after_every_call_valid_comma_separated_string=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      valid = controller._ValidateColumnString("this, that,bla")
      expected = (
          'Column names are not in valid format. Reenter them correctly [name,'
          'name...]')
      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(valid, 'this,that,bla')

  def testCreateSQLQueryModelWithUserInput(self):
    """test the creation of the sql Query model with the user input"""
    query = "select x "
    with_examples = True
    query_execution = fake_sqlite_query_execution.SQLQueryExecution(
        sql_query_data.SQLQueryData(
            data=['first', 'second', 'third', 'fourth'],
            columns=[sql_query_column_model.SQLColumnModel('that')]))

    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), confirm_amount_same=2,
          prompt_info='that,other')
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          assumed_timestamps=['test'],
      )
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      model = controller._CreateSQLQueryModelWithUserInput(
          query, with_examples, query_execution
      )
      expected = (
          'Your query output could look like this.'
          '[\'that\']'
          'first'
          'second'
          'third'
          'Do you want to add this query?'
          'Do you want to name the query parse row:  ?'
          'Is the column a time event? test'
          'Enter (additional) timestamp events from the query [columnName,'
          'aliasName...] or [abort]'
          'At least one timestamp is required, please add a timestamp'
          'Added: that'
          'Failed: other'
          'Do you want to add more timestamps?'
          'Does the event  need customizing?')

      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertFalse(model.needs_customizing)
      self.assertEqual(model.query, query.strip())
      self.assertEqual(model.columns, [])

  def testCreateSQLQueryModelWithUserInputNotAdding(self):
    """test the creation of the sql Query model with the user input"""
    query = "select x"
    with_examples = True
    query_execution = fake_sqlite_query_execution.SQLQueryExecution(
        sql_query_data.SQLQueryData(
            data=['first', 'second', 'third'], columns=[]))

    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), confirm=False)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper()
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      model = controller._CreateSQLQueryModelWithUserInput(
          query, with_examples, query_execution
      )
      expected = ('Your query output could look like this.'
                  '[]'
                  'first'
                  'second'
                  'third'
                  'Do you want to add this query?')

      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertIsNone(model)

  def testGenerateIfConfirmed(self):
    """ test the generate if confirmed"""
    template_path = path_helper.TemplatePath()
    yapf_path = path_helper.YapfStyleFilePath()

    with tempfile.TemporaryDirectory() as tmpdir:
      file = os.path.join(tmpdir, 'testfile')
      pathlib.Path(file).touch()

      fake_execution = fake_sqlite_query_execution.SQLQueryExecution(
          sql_query_data.SQLQueryData(has_error=False, data=[(1, 2)])
      )

      output_handler = output_handler_file.OutputHandlerFile(
          file, file_handler.FileHandler(), confirm=True)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          valid_name=False, change_bool_after_every_call_valid_name=True)
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)

      controller._path = tmpdir
      controller._name = "the_plugin"
      controller._testfile = file
      controller._query_execution = fake_execution
      controller.Generate(template_path, yapf_path)
      file1 = os.path.join(tmpdir, 'plaso', 'formatters', 'the_plugin.py')
      file2 = os.path.join(tmpdir, 'plaso', 'parsers', 'sqlite_plugins',
                           'the_plugin.py')
      file3 = os.path.join(tmpdir, 'tests', 'formatters', 'the_plugin.py')
      file4 = os.path.join(tmpdir, 'tests', 'parsers', 'sqlite_plugins',
                           'the_plugin.py')
      file5 = os.path.join(tmpdir, 'test_data', 'the_plugin.')
      file6 = os.path.join(tmpdir, 'plaso', 'parsers', 'sqlite_plugins',
                           '__init__.py')
      file7 = os.path.join(tmpdir, 'plaso', 'formatters', '__init__.py')
      expected = ('Do you want to Generate the files?create {0}create {1}'
                  'create {2}create {3}copy {4}create {5}create {6}'
                  .format(file1, file2, file3, file4, file5, file6, file7))

      actual = self._ReadFromFile(file)
      self.assertEqual(expected, actual)

  def testGenerateIfNotConfirmed(self):
    """test the generate if confirmed """
    template_path = path_helper.TemplatePath()

    with self.assertRaises(SystemExit):
      with tempfile.TemporaryDirectory() as tmpdir:
        file = os.path.join(tmpdir, 'testfile')
        pathlib.Path(file).touch()

        output_handler = output_handler_file.OutputHandlerFile(
            file, file_handler.FileHandler(), confirm=False)

        plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
            valid_name=False,
            change_bool_after_every_call_valid_name=True)
        controller = sqlite_controller.SQLiteController(output_handler,
                                                        plugin_helper)
        controller.Generate('not used', 'not used')

        self.assertFalse(template_path)

  def testIsDatabaseFolderIfTrue(self):
    """test the function isDatabase if the file is a database"""
    controller = sqlite_controller.SQLiteController(None, None)
    actual = controller._IsDatabaseFile(
        os.path.join(path_helper.TestDatabasePath(), 'twitter_ios.db'))
    self.assertTrue(actual)

  def testIsDatabaseFolderIfFalse(self):
    """test the function isDatabase if the file is not a database"""
    controller = sqlite_controller.SQLiteController(None, None)
    actual = controller._IsDatabaseFile(
        os.path.join(path_helper.TestDatabasePath(), 'twitter_ios_error.db'))
    self.assertFalse(actual)

  def testGetTimestampWithFake(self):
    """test the function GetTimestamp"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_info='that,other',
          confirm_amount_same=1)
      plugin_helper = fake_sqlite_plugin_helper.FakeSQLitePluginHelper(
          assumed_timestamps=['test'],
          columns_and_timestamp_column=(['this'], ['that'])
      )
      controller = sqlite_controller.SQLiteController(output_handler,
                                                      plugin_helper)
      columns = [sql_query_column_model.SQLColumnModel('this'),
                 sql_query_column_model.SQLColumnModel('that'),
                 sql_query_column_model.SQLColumnModel('test')]

      model = controller.GetTimestamps(columns, [])
      expected = (
          'Is the column a time event? '
          'testEnter (additional) timestamp events from the query '
          '[columnName,aliasName...] or [abort]'
          'Added: test,that'
          'Failed: other'
          'Do you want to add more timestamps?')

      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(len(model[0]), 1)
      self.assertEqual(len(model[1]), 1)

  def testGetCustomizableNormal(self):
    """test the function GetCustomizable"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_info='that,other',
          confirm_amount_same=1)

      plugin_helper = sqlite_plugin_helper.SQLitePluginHelper()
      controller = sqlite_controller.SQLiteController(
          output_handler, plugin_helper)

      columns = [sql_query_column_model_data.SQLColumnModelData('this'),
                 sql_query_column_model_data.SQLColumnModelData('that'),
                 sql_query_column_model_data.SQLColumnModelData('test')]

      model = controller.GetCustomizable(columns)
      expected = (
          'Enter columns that are customizable [columnName,aliasName...] '
          'or [abort]'
          'Added: thatFailed: other'
          'Do you want to add more columns that are customizable?'
          'Enter columns that are customizable [columnName,aliasName...] or '
          '[abort]Added: thatFailed: other'
          'Do you want to add more columns that are customizable?')

      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(len(model), 3)
      self.assertEqual(model[0].customize, False)
      self.assertEqual(model[1].customize, True)
      self.assertEqual(model[1].sql_column, 'that')
      self.assertEqual(model[2].customize, False)

  def testGetCustomizableWithAbortToEarly(self):
    """test the function GetCustomizable"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_info_list=['abort', 'this'],
          confirm=False)

      plugin_helper = sqlite_plugin_helper.SQLitePluginHelper()
      controller = sqlite_controller.SQLiteController(
          output_handler, plugin_helper)
      columns = [sql_query_column_model_data.SQLColumnModelData('this'),
                 sql_query_column_model_data.SQLColumnModelData('that'),
                 sql_query_column_model_data.SQLColumnModelData('test')]

      model = controller.GetCustomizable(columns)
      expected = (
          'Enter columns that are customizable [columnName,aliasName...] '
          'or [abort]'
          'At least one column is required, please add a column'
          'Added: thisFailed: '
          'Do you want to add more columns that are customizable?')

      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(len(model), 3)
      self.assertEqual(model[0].customize, True)
      self.assertEqual(model[1].customize, False)
      self.assertEqual(model[2].customize, False)

  def testGetCustomizableWithAbort(self):
    """test the function GetCustomizable"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_info_list=['this', 'abort'],
          prompt_error='this', confirm=True)

      plugin_helper = sqlite_plugin_helper.SQLitePluginHelper()
      controller = sqlite_controller.SQLiteController(
          output_handler, plugin_helper)
      columns = [sql_query_column_model_data.SQLColumnModelData('this'),
                 sql_query_column_model_data.SQLColumnModelData('that'),
                 sql_query_column_model_data.SQLColumnModelData('test')]

      model = controller.GetCustomizable(columns)

      expected = (
          'Enter columns that are customizable [columnName,aliasName...] '
          'or [abort]'
          'Added: thisFailed: '
          'Do you want to add more columns that are customizable?'
          'Enter columns that are customizable [columnName,aliasName...] '
          'or [abort]')

      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(len(model), 3)
      self.assertEqual(model[0].customize, True)
      self.assertEqual(model[1].customize, False)
      self.assertEqual(model[2].customize, False)

  def testGetTimestampNormal(self):
    """test the function GetTimestamp"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_info='thisdate,other,test',
          confirm_amount_same=2)
      plugin_helper = sqlite_plugin_helper.SQLitePluginHelper()
      controller = sqlite_controller.SQLiteController(
          output_handler, plugin_helper)

      columns = [sql_query_column_model.SQLColumnModel('this'),
                 sql_query_column_model.SQLColumnModel('that'),
                 sql_query_column_model.SQLColumnModel('test'),
                 sql_query_column_model.SQLColumnModel('thisdate'),
                 sql_query_column_model.SQLColumnModel('timethat')]

      model = controller.GetTimestamps(columns, [])
      expected = (
          'Is the column a time event? thisdate'
          'Is the column a time event? timethat'
          'Enter (additional) timestamp events from the query '
          '[columnName,aliasName...] or [abort]'
          'Added: test,thisdate,timethat'
          'Failed: other'
          'Do you want to add more timestamps?'
      )
      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(len(model[0]), 2)
      self.assertEqual(len(model[1]), 3)
      self.assertEqual(model[0][0].sql_column, 'this')
      self.assertEqual(model[0][1].sql_column, 'that')
      self.assertEqual(model[1][0].sql_column, 'test')
      self.assertEqual(model[1][1].sql_column, 'thisdate')
      self.assertEqual(model[1][2].sql_column, 'timethat')

  def testGetTimestampNormalWithAbort(self):
    """test the function GetTimestamp"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_info='abort',
          confirm_amount_same=2)
      plugin_helper = sqlite_plugin_helper.SQLitePluginHelper()
      controller = sqlite_controller.SQLiteController(
          output_handler, plugin_helper)

      columns = [sql_query_column_model.SQLColumnModel('this'),
                 sql_query_column_model.SQLColumnModel('that'),
                 sql_query_column_model.SQLColumnModel('test'),
                 sql_query_column_model.SQLColumnModel('thisdate'),
                 sql_query_column_model.SQLColumnModel('timethat')]

      model = controller.GetTimestamps(columns, [])
      expected = (
          'Is the column a time event? thisdate'
          'Is the column a time event? timethat'
          'Enter (additional) timestamp events from the query '
          '[columnName,aliasName...] or [abort]'
      )

      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(len(model[0]), 3)
      self.assertEqual(len(model[1]), 2)
      self.assertEqual(model[0][0].sql_column, 'this')
      self.assertEqual(model[0][1].sql_column, 'that')
      self.assertEqual(model[0][2].sql_column, 'test')
      self.assertEqual(model[1][0].sql_column, 'thisdate')
      self.assertEqual(model[1][1].sql_column, 'timethat')

  def testGetTimestampRefuseATimeEvent(self):
    """test the function GetTimestamp"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_info='test,other',
          confirm_amount_same=1)
      plugin_helper = sqlite_plugin_helper.SQLitePluginHelper()
      controller = sqlite_controller.SQLiteController(
          output_handler, plugin_helper)

      columns = [sql_query_column_model.SQLColumnModel('this'),
                 sql_query_column_model.SQLColumnModel('that'),
                 sql_query_column_model.SQLColumnModel('test'),
                 sql_query_column_model.SQLColumnModel('thisdate'),
                 sql_query_column_model.SQLColumnModel('timethat')]

      model = controller.GetTimestamps(columns, [])
      expected = (
          'Is the column a time event? thisdate'
          'Is the column a time event? timethat'
          'Enter (additional) timestamp events from the query '
          '[columnName,aliasName...] or [abort]'
          'Added: test,thisdate'
          'Failed: other'
          'Do you want to add more timestamps?'
      )

      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(len(model[0]), 3)
      self.assertEqual(len(model[1]), 2)
      self.assertEqual(model[0][0].sql_column, 'this')
      self.assertEqual(model[0][1].sql_column, 'that')
      self.assertEqual(model[0][2].sql_column, 'timethat')
      self.assertEqual(model[1][0].sql_column, 'test')
      self.assertEqual(model[1][1].sql_column, 'thisdate')

  def testGetTimestampRefuseAllTimeEvent(self):
    """test the function GetTimestamp"""
    with tempfile.TemporaryDirectory() as tmpdir:
      path = os.path.join(tmpdir, 'testfile')
      pathlib.Path(path).touch()

      output_handler = output_handler_file.OutputHandlerFile(
          path, file_handler.FileHandler(), prompt_info='test,other',
          confirm=False)
      plugin_helper = sqlite_plugin_helper.SQLitePluginHelper()
      controller = sqlite_controller.SQLiteController(
          output_handler, plugin_helper)

      columns = [sql_query_column_model.SQLColumnModel('this'),
                 sql_query_column_model.SQLColumnModel('that'),
                 sql_query_column_model.SQLColumnModel('test'),
                 sql_query_column_model.SQLColumnModel('thisdate'),
                 sql_query_column_model.SQLColumnModel('timethat')]

      model = controller.GetTimestamps(columns, [])
      expected = (
          'Is the column a time event? this'
          'dateIs the column a time event? timethat'
          'Enter (additional) timestamp events from the query '
          '[columnName,aliasName...] or [abort]'
          'At least one timestamp is required, please add a timestamp'
          'Added: test'
          'Failed: other'
          'Do you want to add more timestamps?'
      )

      actual = self._ReadFromFile(path)
      self.assertEqual(expected, actual)
      self.assertEqual(len(model[0]), 4)
      self.assertEqual(len(model[1]), 1)
      self.assertEqual(model[0][0].sql_column, 'this')
      self.assertEqual(model[0][1].sql_column, 'that')
      self.assertEqual(model[0][2].sql_column, 'thisdate')
      self.assertEqual(model[0][3].sql_column, 'timethat')
      self.assertEqual(model[1][0].sql_column, 'test')

  def _ReadFromFile(self, path: str):
    """Read from file

    Args:
      path (str): the file path

      path (str): the file path

    Returns:
      str: content of the file"""
    with open(path, 'r') as f:
      return f.read()
    os.remove(path)


if __name__ == '__main__':
  unittest.main()
