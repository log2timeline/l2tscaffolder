# -*- coding: utf-8 -*-
# pylint: disable=no-member
# pylint does not recognize connect and close as member
"""Base for sql Query validators"""

from plasoscaffolder.dal import base_database_information


class FakeSQLiteDatabaseInformation(
    base_database_information.BaseDatabaseInformation):
  """Class representing the fake SQLite Database validator """

  def __init__(self, required_tables: [str]):
    """Initializes the fake database information class

    Args:
      required_tables ([str]): the value to return
    """
    super().__init__()
    self._required_tables = required_tables

  def GetTablesFromDatabase(self) -> [str]:
    """Executes the SQL Query.

    Args:
      query (str): The SQL Query to execute on the SQLite database.

    Returns:
      [str]: the names of the tables"""
    return self._required_tables

  def GetTableColumnsAndType(self, table: str, all_lowercase=False) -> [str]:
    """Getting Types for Column if there is are multiple tables

    Args:
      tables ([str]): the name of the table
      column_model ([sql_query_column_model.SQLColumnModel]): the column to
          find the type for
      query (str): the SQL query

    Returns:
      [sql_query_column_model.SQLColumnModel]: the column model with the types,
          or None if there was a prefix error and it could not be parsed
    """
    return {}
