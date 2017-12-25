# -*- coding: utf-8 -*-
"""Information for the SQLite Database."""
from plasoscaffolder.dal import (base_database_information)
from plasoscaffolder.dal import base_sql_query_execution


class SQLiteDatabaseInformation(
    base_database_information.BaseDatabaseInformation):
  """Class representing the SQLite Query validator."""

  def __init__(self,
               sql_execution: base_sql_query_execution.BaseSQLQueryExecution):
    """Initializes the SQL Query Validator.

    Args:
      sql_execution (base_sql_query_execution.BaseSQLQueryExecution): the
          helper to execute a query
    """
    super().__init__()
    self._sql_execution = sql_execution

  def GetTablesFromDatabase(self) -> [str]:
    """Returns all tables from the database

    Returns:
      [str]: the names of the tables
    """
    query = "select name from sqlite_master where type='table' order by name"
    data = self._sql_execution.ExecuteQuery(query)

    if data.has_error:
      return []
    else:
      return [str(data_tuple[0]) for data_tuple in data.data]

  def GetTableColumnsAndType(
      self, table: str, all_lowercase: bool=False
  ) -> [str]:
    """Returns the table information from the database

    Args:
      table (str): the name of the table
      all_lowercase (bool): if the table name and the type should be returned
          in lower case

    Returns:
      {name, type}: the table information, with the name of the column and the
          type of the column
    """
    query = 'PRAGMA table_info({0})'.format(table)
    data = self._sql_execution.ExecuteQuery(query)
    if data.has_error:
      return {}
    else:
      if all_lowercase:
        types = {data_tuple[1].lower(): data_tuple[2].lower() for data_tuple in
                 data.data}
      else:
        types = {data_tuple[1]: data_tuple[2] for data_tuple in data.data}
      return types
