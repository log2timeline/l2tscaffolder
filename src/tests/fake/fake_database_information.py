# -*- coding: utf-8 -*-
# unused argument in a fake is perfectly fine
# pylint: disable=unused-argument
"""Fake class for the Information for the SQLite Database"""


class FakeDatabaseInformation(object):
  """Fake class representing the SQLite Query validator."""

  def __init__(self, tables: [], column_type: {str, type}):
    """Initializes the fake

    Args:
      tables ([str]): the return for the method GetTablesFromDatabase
      column_type ({str, type}): the return for the method
          GetTableColumnsAndType
    """
    self.tables = tables
    self.column_type = column_type

  def GetTablesFromDatabase(self) -> [str]:
    """Executes the SQL Query.

    Returns:
      [str]: the name of the tables
    """
    return self.tables

  def GetTableColumnsAndType(
      self, table: str, all_lowercase=False
  ) -> [{str, type}]:
    """Returns the table information from the database

    Args:
      table (str): the name of the table

    Returns:
      [{str, type}]: the table information first the column and then the type
    """
    return self.column_type
