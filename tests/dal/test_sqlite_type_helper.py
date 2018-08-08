# !/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=protected-access
# because tests should access protected members
"""test class"""
import unittest

from plasoscaffolder.dal import sqlite_type_helper
from plasoscaffolder.model import sql_query_column_model
from tests.fake import fake_database_information, fake_explain_query_plan


class SQLiteQueryExecutionTest(unittest.TestCase):
  """test the SQLite Query execution test"""

  def setUp(self):
    self.sql_type_helper = sqlite_type_helper.SQLiteTypeHelper(None, None, None)

  def testGetDuplicateColumnNamesIfDistinct(self):
    """test a distinct list"""
    columns = list()
    columns.append(sql_query_column_model.SQLColumnModel('a'))
    columns.append(sql_query_column_model.SQLColumnModel('b'))
    columns.append(sql_query_column_model.SQLColumnModel('c'))
    result = self.sql_type_helper.GetDuplicateColumnNames(columns)
    expected = []
    self.assertEqual(result, expected)

  def testGetDuplicateColumnNamesIfOneDuplicate(self):
    """test a duplicate list with one duplicate"""
    columns = list()
    columns.append(sql_query_column_model.SQLColumnModel('a'))
    columns.append(sql_query_column_model.SQLColumnModel('a'))
    columns.append(sql_query_column_model.SQLColumnModel('b'))
    columns.append(sql_query_column_model.SQLColumnModel('c'))
    result = self.sql_type_helper.GetDuplicateColumnNames(columns)
    expected = ['a']
    self.assertEqual(result, expected)

  def testGetDuplicateColumnNamesIfMultipleDuplicates(self):
    """test a duplicate list with multiple duplicates"""
    columns = list()
    columns.append(sql_query_column_model.SQLColumnModel('a'))
    columns.append(sql_query_column_model.SQLColumnModel('a'))
    columns.append(sql_query_column_model.SQLColumnModel('a'))
    columns.append(sql_query_column_model.SQLColumnModel('b'))
    columns.append(sql_query_column_model.SQLColumnModel('b'))
    columns.append(sql_query_column_model.SQLColumnModel('c'))
    result = self.sql_type_helper.GetDuplicateColumnNames(columns)
    expected = ['a', 'b']
    self.assertEqual(result, expected)

  def testGetColumnDescriptionWithElements(self):
    """test getting column description if description is not empty."""
    description = [['this', 'that'], ['second', 23, 'hat']]
    result = self.sql_type_helper.GetColumnInformationFromDescription(
        description)

    self.assertEqual(len(result), 2)
    self.assertEqual(result[0].sql_column, 'this')
    self.assertEqual(result[0].sql_column_type, type(None))
    self.assertEqual(result[1].sql_column, 'second')
    self.assertEqual(result[1].sql_column_type, type(None))

  def testGetColumnDescriptionEmpty(self):
    """test getting column description if description is empty."""
    description = []
    result = self.sql_type_helper.GetColumnInformationFromDescription(
        description)
    self.assertEqual(len(result), 0)
    self.assertEqual(result, [])

  def testGetColumnDescriptionNone(self):
    """test getting column description if description is none."""
    description = None
    result = self.sql_type_helper.GetColumnInformationFromDescription(
        description)
    self.assertEqual(len(result), 0)
    self.assertEqual(result, [])

  def testGetPositionAfterSeparatorSpace(self):
    """test getting position after space"""
    text = 'this is a db.test'
    end = len(text)
    result = self.sql_type_helper._GetPositionAfterSeparator(text, end)
    expected = len(text) - len('db.text')
    self.assertEqual(result, expected)

  def testGetPositionAfterSeparatorComma(self):
    """test getting position after comma"""
    text = 'this is a,db.test'
    end = len(text)
    result = self.sql_type_helper._GetPositionAfterSeparator(text, end)
    expected = len(text) - len('db.text')
    self.assertEqual(result, expected)

  def testGetPositionAfterSeparatorCommaAndSpace(self):
    """test getting position after comma and space."""
    text = 'this is a ,db.test'
    end = len(text)
    result = self.sql_type_helper._GetPositionAfterSeparator(text, end)
    expected = len(text) - len('db.text')
    self.assertEqual(result, expected)

  def testGetPositionAfterSeparatorCommaAndSpaceAfter(self):
    """test getting position after comma and space afterwards"""
    text = 'this is a, db.test'
    end = len(text)
    result = self.sql_type_helper._GetPositionAfterSeparator(text, end)
    expected = len(text) - len('db.text')
    self.assertEqual(result, expected)

  def testGetPositionAfterSeparatorCommaAndSpaceBeforeAndAfter(self):
    """test getting position after comma and space before and after comma"""
    text = 'this is a , db.test'
    end = len(text)
    result = self.sql_type_helper._GetPositionAfterSeparator(text, end)
    expected = len(text) - len('db.text')
    self.assertEqual(result, expected)

  def testGetPositionAfterSeparatorCommaAndMultipleSpaceBeforeAndAfter(self):
    """test getting position after comma and multiple space before and after
    comma"""
    text = 'this is a  ,   db.test'
    end = len(text)
    result = self.sql_type_helper._GetPositionAfterSeparator(text, end)
    expected = len(text) - len('db.text')
    self.assertEqual(result, expected)

  def testGetEndOfTableIfNotAliasEasy(self):
    """test get the end of a table with easy query"""
    text = 'select db.id from db'
    result = self.sql_type_helper._GetEndOfTableIfNotAlias(text, 'id')
    expected = len('select db')
    self.assertEqual(result, expected)

  def testGetEndOfTableIfNotAliasWithAliasAfterWithSpace(self):
    """test get the end of a table with alias after"""
    text = 'select db.id, x.id as another from db'
    result = self.sql_type_helper._GetEndOfTableIfNotAlias(text, 'id')
    expected = len('select db')
    self.assertEqual(result, expected)

  def testGetEndOfTableIfNotAliasWithAliasAfterWithComma(self):
    """test get the end of a table with alias after"""
    text = 'select db.id,x.id as another from db'
    result = self.sql_type_helper._GetEndOfTableIfNotAlias(text, 'id')
    expected = len('select db')
    self.assertEqual(result, expected)

  def testGetEndOfTableIfNotAliasWithAliasBefore(self):
    """test get the end of a table with alias before"""
    text = 'select db.id as this, db2.id from db join db2'
    result = self.sql_type_helper._GetEndOfTableIfNotAlias(text, 'id')
    expected = len('select db.id as this, db2')
    self.assertEqual(result, expected)

  def testGetEndOfTableIfNotAliasWithMultipleAliasBefore(self):
    """test get the end of a table with alias before"""
    text = ('select db.id as this db3.id as that, db4.id as here, db2.id '
            'from db join db2')
    result = self.sql_type_helper._GetEndOfTableIfNotAlias(text, 'id')
    expected = len('select db.id as this db3.id as that, db4.id as here, db2')
    self.assertEqual(result, expected)

  def testGetEndOfTableIfNotAliasWithOnlyAlias(self):
    """test get the end of a table with only an alias"""
    text = 'select x.id as another from db'
    result = self.sql_type_helper._GetEndOfTableIfNotAlias(text, 'id')
    expected = 0
    self.assertEqual(result, expected)

  def testColumnTypeForOnlyOneTable(self):
    """test getting the column type for only one table"""
    mappings = {'id': 'float', 'that': 'varchar', 'different': 'integer',
                'bla': 'real'}
    self.sql_type_helper._information = (
        fake_database_information.FakeDatabaseInformation(None, mappings))

    model = [sql_query_column_model.SQLColumnModel('id'),
             sql_query_column_model.SQLColumnModel('that'),
             sql_query_column_model.SQLColumnModel('different'),
             sql_query_column_model.SQLColumnModel('bla')]
    result = self.sql_type_helper._ColumnTypeForMultipleTables(
        'other', model, '')
    self.assertEqual(len(result), 4)
    self.assertEqual(result[0].sql_column, 'id')
    self.assertEqual(result[1].sql_column, 'that')
    self.assertEqual(result[2].sql_column, 'different')
    self.assertEqual(result[3].sql_column, 'bla')
    self.assertEqual(result[0].sql_column_type, float)
    self.assertEqual(result[1].sql_column_type, str)
    self.assertEqual(result[2].sql_column_type, int)
    self.assertEqual(result[3].sql_column_type, float)

  def testColumnTypeForMultipleTables(self):
    """test getting the column type for multiple table"""
    mappings = {'id': 'blob', 'that': 'varchar', 'different': 'integer'}
    tables = ['db1', 'db2', 'db3']
    query = ('select db1.id , db2.that, db1.different,db2.id as id2, db3.id as '
             'id3 from db1 join db2 join db3')
    self.sql_type_helper._information = (
        fake_database_information.FakeDatabaseInformation(None, mappings))

    model = [sql_query_column_model.SQLColumnModel('id'),
             sql_query_column_model.SQLColumnModel('that'),
             sql_query_column_model.SQLColumnModel('different'),
             sql_query_column_model.SQLColumnModel('id2'),
             sql_query_column_model.SQLColumnModel('id3')]
    result = self.sql_type_helper._ColumnTypeForMultipleTables(
        tables, model, query)
    self.assertEqual(len(result), 5)
    self.assertEqual(result[0].sql_column, 'id')
    self.assertEqual(result[1].sql_column, 'that')
    self.assertEqual(result[2].sql_column, 'different')
    self.assertEqual(result[3].sql_column, 'id2')
    self.assertEqual(result[4].sql_column, 'id3')
    self.assertEqual(result[0].sql_column_type, bytes)
    self.assertEqual(result[1].sql_column_type, str)
    self.assertEqual(result[2].sql_column_type, int)
    self.assertEqual(result[3].sql_column_type, bytes)
    self.assertEqual(result[4].sql_column_type, bytes)

  def testAddMissingTypesFromSchemaForOnlyOneTable(self):
    """test getting missing types from schema if only one table"""
    mappings = {'id': 'float', 'that': 'varchar', 'different': 'integer',
                'bla': 'real'}
    query = "select id, that, db.different, bla from db"
    tables = ['db']
    self.sql_type_helper._explain = (
        fake_explain_query_plan.FakeExplainQueryPlan(locked_tables=tables))
    self.sql_type_helper._information = (
        fake_database_information.FakeDatabaseInformation(tables, mappings))

    model = [sql_query_column_model.SQLColumnModel('id'),
             sql_query_column_model.SQLColumnModel('that'),
             sql_query_column_model.SQLColumnModel('different'),
             sql_query_column_model.SQLColumnModel('bla')]

    result = self.sql_type_helper.AddMissingTypesFromSchema(model, query)
    self.assertEqual(len(result), 4)
    self.assertEqual(result[0].sql_column, 'id')
    self.assertEqual(result[1].sql_column, 'that')
    self.assertEqual(result[2].sql_column, 'different')
    self.assertEqual(result[3].sql_column, 'bla')
    self.assertEqual(result[0].sql_column_type, float)
    self.assertEqual(result[1].sql_column_type, str)
    self.assertEqual(result[2].sql_column_type, int)
    self.assertEqual(result[3].sql_column_type, float)

  def testAddMissingTypesFromSchemaForMultipleOneTable(self):
    """test getting missing types from schema multiple tables"""
    mappings = {'id': 'blob', 'that': 'varchar', 'different': 'integer'}
    tables = ['db1', 'db2', 'db3']
    query = ('select db1.id , db2.that, db1.different,db2.id as id2, db3.id as '
             'id3 from db1 join db2 join db3')
    self.sql_type_helper._information = (
        fake_database_information.FakeDatabaseInformation(tables, mappings))
    self.sql_type_helper._explain = (
        fake_explain_query_plan.FakeExplainQueryPlan(locked_tables=tables))
    model = [sql_query_column_model.SQLColumnModel('id'),
             sql_query_column_model.SQLColumnModel('that'),
             sql_query_column_model.SQLColumnModel('different'),
             sql_query_column_model.SQLColumnModel('id2'),
             sql_query_column_model.SQLColumnModel('id3')]
    result = self.sql_type_helper.AddMissingTypesFromSchema(model, query)

    self.assertEqual(len(result), 5)
    self.assertEqual(result[0].sql_column, 'id')
    self.assertEqual(result[1].sql_column, 'that')
    self.assertEqual(result[2].sql_column, 'different')
    self.assertEqual(result[3].sql_column, 'id2')
    self.assertEqual(result[4].sql_column, 'id3')
    self.assertEqual(result[0].sql_column_type, bytes)
    self.assertEqual(result[1].sql_column_type, str)
    self.assertEqual(result[2].sql_column_type, int)
    self.assertEqual(result[3].sql_column_type, bytes)
    self.assertEqual(result[4].sql_column_type, bytes)

  if __name__ == '__main__':
    unittest.main()
