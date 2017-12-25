# !/usr/bin/python
# -*- coding: utf-8 -*-
"""test class"""
import unittest

from plasoscaffolder.model import sql_query_column_model


class SQLColumnModelTest(unittest.TestCase):
  """test class for SQLColumnModel"""

  def testColumnAsSnakeCaseLongNameCamelCase(self):
    """Test snake case for a long name with camel case."""
    column = sql_query_column_model.SQLColumnModel('theOneLongColumnName')
    actual = column.GetColumnAsSnakeCase()
    expected = 'the_one_long_column_name'
    self.assertEqual(actual, expected)

  def testColumnAsSnakeCaseLongNamePascalCase(self):
    """Test snake case for for a long name with pascal case."""
    column = sql_query_column_model.SQLColumnModel('TheOneLongColumnName')
    actual = column.GetColumnAsSnakeCase()
    expected = 'the_one_long_column_name'
    self.assertEqual(actual, expected)

  def testColumnAsSnakeCaseShortName(self):
    """Test snake case for a short name only small letters."""
    column = sql_query_column_model.SQLColumnModel('short')
    actual = column.GetColumnAsSnakeCase()
    expected = 'short'
    self.assertEqual(actual, expected)

  def testColumnAsSnakeCaseWithNumber(self):
    """Test snake case for a short name only small letters."""
    column = sql_query_column_model.SQLColumnModel('int2val')
    actual = column.GetColumnAsSnakeCase()
    expected = 'int2val'
    self.assertEqual(actual, expected)

  def testColumnAsSnakeCaseStartWithNumber(self):
    """Test snake case for a name with numbers resulting in an error."""
    column = sql_query_column_model.SQLColumnModel('123error')
    actual = column.GetColumnAsSnakeCase()
    expected = '123error'
    self.assertEqual(actual, expected)

  def testColumnAsSnakeCaseHasUnderline(self):
    """Test column as description for a name ending with an underscore
    resulting in an error."""
    column = sql_query_column_model.SQLColumnModel('error_')
    actual = column.GetColumnAsSnakeCase()
    expected = 'error_'
    self.assertEqual(actual, expected)

  def testColumnAsDescriptionLongNameCamelCase(self):
    """Test column as description for a long name with camel case."""
    column = sql_query_column_model.SQLColumnModel('theOneLongColumnName')
    actual = column.GetColumnAsDescription()
    expected = 'The One Long Column Name'
    self.assertEqual(actual, expected)

  def testColumnAsDescriptionLongNamePascalCase(self):
    """Test column as description for a long name with pascal case."""
    column = sql_query_column_model.SQLColumnModel('TheOneLongColumnName')
    actual = column.GetColumnAsDescription()
    expected = 'The One Long Column Name'
    self.assertEqual(actual, expected)

  def testColumnAsDescriptionShortName(self):
    """Test column as description for a short name."""
    column = sql_query_column_model.SQLColumnModel('short')
    actual = column.GetColumnAsDescription()
    expected = 'Short'
    self.assertEqual(actual, expected)

  def testColumnTypeAsNameString(self):
    """Test getting the type for a string."""
    column = sql_query_column_model.SQLColumnModel('string', str)

    actual_type = column.sql_column_type
    expected_type = str
    actual = column.GetColumnTypeAsName()
    expected = 'str'
    self.assertEqual(actual_type, expected_type)
    self.assertEqual(actual, expected)

  def testColumnTypeAsNameInt(self):
    """Test getting the type for an int"""
    column = sql_query_column_model.SQLColumnModel('string', int)

    actual_type = column.sql_column_type
    expected_type = int
    actual = column.GetColumnTypeAsName()
    expected = 'int'
    self.assertEqual(actual_type, expected_type)
    self.assertEqual(actual, expected)




if __name__ == '__main__':
  unittest.main()
