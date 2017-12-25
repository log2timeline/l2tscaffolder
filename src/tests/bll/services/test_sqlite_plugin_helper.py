# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test class"""
import os
import tempfile
import unittest

from plasoscaffolder.bll.services import sqlite_plugin_helper
from plasoscaffolder.dal import sql_query_data
from plasoscaffolder.model import sql_query_column_model
from plasoscaffolder.model import sql_query_model
from tests.fake import fake_sqlite_plugin_path_helper
from tests.fake import fake_sqlite_query_execution
from tests.test_helper import path_helper


class SQLitePluginHelperTest(unittest.TestCase):
  """  Class representing a test case testing the SQLite plugin helper"""

  def setUp(self):
    self.helper = sqlite_plugin_helper.SQLitePluginHelper()
    self.template_path = path_helper.TemplatePath()

  def test_PluginExistsIfFalse(self):
    """Tests the plugin exists method if none exists."""
    actual = self.helper.PluginExists(
        'temp', 'plugin_test', 'db',
        fake_sqlite_plugin_path_helper.FakeSQLitePluginPathHelper(
            self.template_path, 'test', 'db'))
    self.assertFalse(actual)

  def test_PluginExistsIfTrue(self):
    """Tests the plugin exists"""
    with tempfile.TemporaryDirectory() as tmpdir:
      file_path = os.path.join(tmpdir, 'test')
      new_file = open(file_path, 'a')
      actual = self.helper.PluginExists(
          tmpdir, new_file.name, 'db',
          fake_sqlite_plugin_path_helper.FakeSQLitePluginPathHelper(
              self.template_path, new_file.name, 'db'))
      new_file.close()
      os.remove(file_path)

    self.assertTrue(actual)

  def test_FileExistsIfTrue(self):
    """ test the method that checks if the file exists """
    with tempfile.TemporaryDirectory() as tmpdir:
      with tempfile.TemporaryFile(dir=tmpdir) as fp:
        actual = self.helper.FileExists(fp.name)
    self.assertTrue(actual)

  def testFolderExistsIfTrue(self):
    """test the method that checks if folder exists"""
    with tempfile.TemporaryDirectory() as tmpdir:
      actual = self.helper.FolderExists(tmpdir)
    self.assertTrue(actual)

  def testRunSQLQuery(self):
    """test run sql query"""
    data = sql_query_data.SQLQueryData(
        columns=[], data=[], has_error=False, error_message=None)
    executor = fake_sqlite_query_execution.SQLQueryExecution(data)
    actual = self.helper.RunSQLQuery('my query', executor)
    self.assertFalse(actual.has_error)
    self.assertIsNone(actual.error_message)
    self.assertEqual(actual.columns, [])
    self.assertEqual(actual.data, [])

  def testIsValidPluginNameExpected(self):
    """tests the plugin Name validation."""
    plugin_name = "this_is_a_test"
    actual = self.helper.IsValidPluginName(plugin_name)
    self.assertTrue(actual)

  def testIsValidPluginNameWithEndingUnderscore(self):
    """tests the plugin Name validation."""
    plugin_name = "this_is_a_"
    actual = self.helper.IsValidPluginName(plugin_name)
    self.assertFalse(actual)

  def testIsValidPluginNameOnlyOneWordLowercase(self):
    """tests the plugin Name validation."""
    plugin_name = "this"
    actual = self.helper.IsValidPluginName(plugin_name)
    self.assertTrue(actual)

  def testIsValidPluginNameOneWordUppercase(self):
    """tests the plugin Name validation."""
    plugin_name = "This"
    actual = self.helper.IsValidPluginName(plugin_name)
    self.assertFalse(actual)

  def testIsValidPluginNameWithNumber(self):
    """tests the plugin Name validation."""
    plugin_name = "this3"
    actual = self.helper.IsValidPluginName(plugin_name)
    self.assertFalse(actual)

  def testGetDistinctColumnsFromSQLQueryData(self):
    """test the creating of a distinct list of all attributes of the queries"""
    queries = list()
    column1 = sql_query_model.SQLQueryModel(
        columns=[sql_query_column_model.SQLColumnModel('createdDate'),
                 sql_query_column_model.SQLColumnModel('updatedAt'),
                 sql_query_column_model.SQLColumnModel('screenName')],
        timestamp_columns=[],
        query="", name="", needs_customizing=False, amount_events=0)
    column2 = sql_query_model.SQLQueryModel(
        columns=[sql_query_column_model.SQLColumnModel('profileImageUrl'),
                 sql_query_column_model.SQLColumnModel('screenName'),
                 sql_query_column_model.SQLColumnModel('userId')],
        timestamp_columns=[],
        query="", name="", needs_customizing=False, amount_events=0)
    column3 = sql_query_model.SQLQueryModel(
        columns=[sql_query_column_model.SQLColumnModel('screenName'),
                 sql_query_column_model.SQLColumnModel('createdDate'),
                 sql_query_column_model.SQLColumnModel('createdDate')],
        timestamp_columns=[],
        query="", name="", needs_customizing=False, amount_events=0)
    column4 = sql_query_model.SQLQueryModel(
        columns=[sql_query_column_model.SQLColumnModel('screenNameSecond'),
                 sql_query_column_model.SQLColumnModel('createdDate')],
        timestamp_columns=[],
        query="", name="", needs_customizing=False, amount_events=0)
    queries.append(column1)
    queries.append(column2)
    queries.append(column3)
    queries.append(column4)
    actual = self.helper.GetDistinctColumnsFromSQLQueryData(queries)
    expected = ['created_date', 'profile_image_url', 'screen_name',
                'screen_name_second', 'updated_at', 'user_id']

    self.assertEqual(actual, expected)

  def testGetDistinctColumnsFromSQLQueryDataEmpty(self):
    """test the creating of a distinct list of all attributes of the queries
    with an empty array"""
    queries = list()
    column1 = sql_query_model.SQLQueryModel(
        columns=[], timestamp_columns=[], query="", name="",
        needs_customizing=False, amount_events=0)
    column2 = sql_query_model.SQLQueryModel(
        columns=[sql_query_column_model.SQLColumnModel('first')],
        timestamp_columns=[], query="", name="", needs_customizing=False,
        amount_events=0)
    queries.append(column1)
    queries.append(column2)
    actual = self.helper.GetDistinctColumnsFromSQLQueryData(queries)
    expected = ['first']
    self.assertEqual(actual, expected)

  def testGetDistinctColumnsFromSQLQueryQueryEmpty(self):
    """test the creating of a distinct list of all attributes of the queries
    with an empty array"""
    queries = list()
    actual = self.helper.GetDistinctColumnsFromSQLQueryData(queries)
    expected = []
    self.assertEqual(actual, expected)

  def testIsValidRowNameShort(self):
    """test the row name for its validity"""
    actual = self.helper.IsValidRowName('Short')
    self.assertTrue(actual)

  def testIsValidRowNameLong(self):
    """test the row name for its validity"""
    actual = self.helper.IsValidRowName('ThisIsALongRowName')
    self.assertTrue(actual)

  def testIsValidRowNameWithErrorLowerCase(self):
    """test the row name for its validity"""
    actual = self.helper.IsValidRowName('wrong')
    self.assertFalse(actual)

  def testIsValidRowNameWithErrorNumber(self):
    """test the row name for its validity"""
    actual = self.helper.IsValidRowName('Row12')
    self.assertFalse(actual)

  def testIsValidCommaSeparatedStringShortCapitalLetterStart(self):
    """test a comma separated string for its validity"""
    actual = self.helper.IsValidCommaSeparatedString('Short1234')
    self.assertTrue(actual)

  def testIsValidCommaSeparatedStringShortLowercaseLetterStart(self):
    """test a comma separated string for its validity"""
    actual = self.helper.IsValidCommaSeparatedString('short1234')
    self.assertTrue(actual)

  def testIsValidCommaSeparatedStringShortNumberStart(self):
    """test a comma separated string for its validity"""
    actual = self.helper.IsValidCommaSeparatedString('123asdgf')
    self.assertTrue(actual)

  def testIsValidCommaSeparatedStringLong(self):
    """test a comma separated string for its validity"""
    actual = self.helper.IsValidCommaSeparatedString('test,213this,Hello')
    self.assertTrue(actual)

  def testIsValidCommaSeparatedStringLongErrorSpace(self):
    """test a comma separated string for its validity"""
    actual = self.helper.IsValidCommaSeparatedString('test, 213this,Hello')
    self.assertFalse(actual)

  def testIsValidCommaSeparatedStringErrorSpace(self):
    """test a comma separated string for its validity"""
    actual = self.helper.IsValidCommaSeparatedString('test, ')
    self.assertFalse(actual)

  def testIsValidCommaSeparatedStringErrorSpaceTwoWords(self):
    """test a comma separated string for its validity"""
    actual = self.helper.IsValidCommaSeparatedString('test, test2')
    self.assertFalse(actual)

  def testIsValidCommaSeparatedStringLongErrorComma(self):
    """test a comma separated string for its validity"""
    actual = self.helper.IsValidCommaSeparatedString('test, 213this,Hello,')
    self.assertFalse(actual)

  def testGetAssumedTimestamps(self):
    """test the the parsing of assumed timestamps"""
    columns = [sql_query_column_model.SQLColumnModel('not'),
               sql_query_column_model.SQLColumnModel('usertime'),
               sql_query_column_model.SQLColumnModel('timecreation'),
               sql_query_column_model.SQLColumnModel('date'),
               sql_query_column_model.SQLColumnModel('time'),
               sql_query_column_model.SQLColumnModel('DaTe'),
               sql_query_column_model.SQLColumnModel('TiMe'),
               sql_query_column_model.SQLColumnModel('userdate'),
               sql_query_column_model.SQLColumnModel('datecreation')]

    actual = self.helper.GetAssumedTimestamps(columns)
    expected = ['usertime', 'timecreation', 'date', 'time', 'DaTe', 'TiMe',
                'userdate', 'datecreation']
    self.assertEqual(actual, expected)

  def testGetAssumedTimestampsEmpty(self):
    """test the the parsing of assumed timestamps"""
    helper = sqlite_plugin_helper.SQLitePluginHelper()
    actual = helper.GetAssumedTimestamps([])
    expected = []
    self.assertEqual(actual, expected)

  def testGetColumnsAndTimestampColumnWithData(self):
    """test the getting of the column and timestamp column"""
    timestamps = ['this', 'that', 'another']
    columns = [sql_query_column_model.SQLColumnModel('not'),
               sql_query_column_model.SQLColumnModel('this'),
               sql_query_column_model.SQLColumnModel('another'),
               sql_query_column_model.SQLColumnModel('that'),
               sql_query_column_model.SQLColumnModel('alsonot')]

    actual = self.helper.GetColumnsAndTimestampColumn(columns, timestamps, [
        ['first', 'second', 'third', 'fourth', 'fifth'],
        ['the', 'next', 'data', 'row', 'things'],
        ['last', 'stuff', 'and', 'some', 'thing']])

    self.assertEqual(len(actual), 2)
    self.assertEqual(len(actual[0]), 2)
    self.assertEqual(len(actual[1]), 3)

    self.assertEqual(actual[0][0].sql_column, 'not')
    self.assertEqual(actual[0][1].sql_column, 'alsonot')
    self.assertEqual(actual[1][0].sql_column, 'this')
    self.assertEqual(actual[1][1].sql_column, 'another')
    self.assertEqual(actual[1][2].sql_column, 'that')
    self.assertEqual(actual[1][0].timestamp, 'second')
    self.assertEqual(actual[1][1].timestamp, 'data')
    self.assertEqual(actual[1][2].timestamp, 'some')
    self.assertEqual(actual[0][0].GetFirstDataForTimeEvent('this'), 'first')
    self.assertEqual(actual[0][0].GetFirstDataForTimeEvent('that'), 'last')
    self.assertEqual(actual[0][0].GetFirstDataForTimeEvent('another'), 'the')
    self.assertEqual(actual[0][1].GetFirstDataForTimeEvent('this'), 'fifth')
    self.assertEqual(actual[0][1].GetFirstDataForTimeEvent('that'), 'thing')
    self.assertEqual(actual[0][1].GetFirstDataForTimeEvent('another'), 'things')
    self.assertEqual(actual[1][0].expected_message, 'Not: first Alsonot: fifth')
    self.assertEqual(actual[1][1].expected_message, 'Not: the Alsonot: things')
    self.assertEqual(actual[1][2].expected_message, 'Not: last Alsonot: thing')

  def testGetColumnsAndTimestampColumnWithNoData(self):
    """test the getting of the column and timestamp column"""
    timestamps = ['this', 'that', 'another']
    columns = [
        sql_query_column_model.SQLColumnModel('not'),
        sql_query_column_model.SQLColumnModel('this'),
        sql_query_column_model.SQLColumnModel('another'),
        sql_query_column_model.SQLColumnModel('that'),
        sql_query_column_model.SQLColumnModel('alsonot')
    ]

    actual = self.helper.GetColumnsAndTimestampColumn(columns, timestamps, [])

    self.assertEqual(len(actual), 2)
    self.assertEqual(len(actual[0]), 2)
    self.assertEqual(len(actual[1]), 3)

    self.assertEqual(actual[0][0].sql_column, 'not')
    self.assertEqual(actual[0][1].sql_column, 'alsonot')
    self.assertEqual(actual[1][0].sql_column, 'this')
    self.assertEqual(actual[1][1].sql_column, 'another')
    self.assertEqual(actual[1][2].sql_column, 'that')
    self.assertEqual(actual[1][0].timestamp, '')
    self.assertEqual(actual[1][1].timestamp, '')
    self.assertEqual(actual[1][2].timestamp, '')
    self.assertEqual(actual[1][0].expected_message, 'Not:  Alsonot: ')
    self.assertEqual(actual[1][1].expected_message, 'Not:  Alsonot: ')
    self.assertEqual(actual[1][2].expected_message, 'Not:  Alsonot: ')
    self.assertEqual(actual[0][0].GetFirstDataForTimeEvent('this'), '')
    self.assertEqual(actual[0][0].GetFirstDataForTimeEvent('that'), '')
    self.assertEqual(actual[0][0].GetFirstDataForTimeEvent('another'), '')
    self.assertEqual(actual[0][1].GetFirstDataForTimeEvent('this'), '')
    self.assertEqual(actual[0][1].GetFirstDataForTimeEvent('that'), '')
    self.assertEqual(actual[0][1].GetFirstDataForTimeEvent('another'), '')

  def testGetColumnsAndTimestampColumnWithOneDataRowForThreeTimestamps(self):
    """test the getting of the column and timestamp column"""
    timestamps = ['this', 'that', 'another']
    columns = [
        sql_query_column_model.SQLColumnModel('not'),
        sql_query_column_model.SQLColumnModel('this'),
        sql_query_column_model.SQLColumnModel('another'),
        sql_query_column_model.SQLColumnModel('that'),
        sql_query_column_model.SQLColumnModel('alsonot')
    ]

    actual = self.helper.GetColumnsAndTimestampColumn(
        columns, timestamps, [['first', 'second', 'third', 'fourth', 'fifth']])

    self.assertEqual(len(actual), 2)
    self.assertEqual(len(actual[0]), 2)
    self.assertEqual(len(actual[1]), 3)

    self.assertEqual(actual[0][0].sql_column, 'not')
    self.assertEqual(actual[0][1].sql_column, 'alsonot')
    self.assertEqual(actual[1][0].sql_column, 'this')
    self.assertEqual(actual[1][1].sql_column, 'another')
    self.assertEqual(actual[1][2].sql_column, 'that')
    self.assertEqual(actual[1][0].timestamp, 'second')
    self.assertEqual(actual[1][1].timestamp, 'third')
    self.assertEqual(actual[1][2].timestamp, 'fourth')
    self.assertEqual(actual[1][0].expected_message, 'Not: first Alsonot: fifth')
    self.assertEqual(actual[1][1].expected_message, 'Not: first Alsonot: fifth')
    self.assertEqual(actual[1][2].expected_message, 'Not: first Alsonot: fifth')
    self.assertEqual(actual[0][0].GetFirstDataForTimeEvent('this'), 'first')
    self.assertEqual(actual[0][0].GetFirstDataForTimeEvent('that'), 'first')
    self.assertEqual(actual[0][0].GetFirstDataForTimeEvent('another'), 'first')
    self.assertEqual(actual[0][1].GetFirstDataForTimeEvent('this'), 'fifth')
    self.assertEqual(actual[0][1].GetFirstDataForTimeEvent('that'), 'fifth')
    self.assertEqual(actual[0][1].GetFirstDataForTimeEvent('another'), 'fifth')

  def testGetColumnsAndTimestampColumnWithTwoDataRowForThreeTimestamps(self):
    """test the getting of the column and timestamp column"""
    timestamps = ['this', 'that', 'another']
    columns = [
        sql_query_column_model.SQLColumnModel('not'),
        sql_query_column_model.SQLColumnModel('this'),
        sql_query_column_model.SQLColumnModel('another'),
        sql_query_column_model.SQLColumnModel('that'),
        sql_query_column_model.SQLColumnModel('alsonot')
    ]

    actual = self.helper.GetColumnsAndTimestampColumn(
        columns, timestamps, [['first', 'second', 'third', 'fourth', 'fifth'],
                              ['the', 'next', 'data', 'row', 'things']])

    self.assertEqual(len(actual), 2)
    self.assertEqual(len(actual[0]), 2)
    self.assertEqual(len(actual[1]), 3)

    self.assertEqual(actual[0][0].sql_column, 'not')
    self.assertEqual(actual[0][1].sql_column, 'alsonot')
    self.assertEqual(actual[1][0].sql_column, 'this')
    self.assertEqual(actual[1][1].sql_column, 'another')
    self.assertEqual(actual[1][2].sql_column, 'that')
    self.assertEqual(actual[1][0].timestamp, 'second')
    self.assertEqual(actual[1][1].timestamp, 'data')
    self.assertEqual(actual[1][2].timestamp, 'row')
    self.assertEqual(actual[1][0].expected_message, 'Not: first Alsonot: fifth')
    self.assertEqual(actual[1][1].expected_message, 'Not: the Alsonot: things')
    self.assertEqual(actual[1][2].expected_message, 'Not: the Alsonot: things')
    self.assertEqual(actual[0][0].GetFirstDataForTimeEvent('this'), 'first')
    self.assertEqual(actual[0][0].GetFirstDataForTimeEvent('that'), 'the')
    self.assertEqual(actual[0][0].GetFirstDataForTimeEvent('another'), 'the')
    self.assertEqual(actual[0][1].GetFirstDataForTimeEvent('this'), 'fifth')
    self.assertEqual(actual[0][1].GetFirstDataForTimeEvent('that'), 'things')
    self.assertEqual(actual[0][1].GetFirstDataForTimeEvent('another'), 'things')

  def testGetColumnsAndTimestampColumnEmptyTimestamp(self):
    """test the getting of the column and timestamp column"""
    columns = [
        sql_query_column_model.SQLColumnModel('not'),
        sql_query_column_model.SQLColumnModel('this'),
        sql_query_column_model.SQLColumnModel('another'),
        sql_query_column_model.SQLColumnModel('that'),
        sql_query_column_model.SQLColumnModel('alsonot')
    ]

    actual = self.helper.GetColumnsAndTimestampColumn(columns, [], [])

    self.assertEqual(len(actual), 2)
    self.assertEqual(len(actual[0]), 5)
    self.assertEqual(len(actual[1]), 0)

    self.assertEqual(actual[0][0].sql_column, 'not')
    self.assertEqual(actual[0][1].sql_column, 'this')
    self.assertEqual(actual[0][2].sql_column, 'another')
    self.assertEqual(actual[0][3].sql_column, 'that')
    self.assertEqual(actual[0][4].sql_column, 'alsonot')

  def testGetColumnsAndTimestampColumnEmptyColumns(self):
    """test the getting of the column and timestamp column"""
    timestamps = ['this', 'that', 'another']
    actual = self.helper.GetColumnsAndTimestampColumn([], timestamps, [])

    self.assertEqual(len(actual), 2)
    self.assertEqual(len(actual[0]), 0)
    self.assertEqual(len(actual[0]), 0)

  def testGetColumnsAndTimestampColumnEmpty(self):
    """test the getting of the column and timestamp column"""
    actual = self.helper.GetColumnsAndTimestampColumn([], [], [])

    self.assertEqual(len(actual), 2)
    self.assertEqual(len(actual[0]), 0)
    self.assertEqual(len(actual[0]), 0)


if __name__ == '__main__':
  unittest.main()
