# -*- coding: utf-8 -*-
"""SQLite Type Helper."""
import collections
import re

from plasoscaffolder.common import type_mapper
from plasoscaffolder.dal import base_database_information
from plasoscaffolder.dal import base_explain_query_plan
from plasoscaffolder.dal import base_sql_query_execution
from plasoscaffolder.dal import base_type_helper
from plasoscaffolder.model import sql_query_column_model


class SQLiteTypeHelper(base_type_helper.BaseTypeHelper):
  """Class representing the type helper for SQLite."""
  _POSSIBLEQUERYSEPERATOR = [' ', ',']

  def __init__(
      self, execution: base_sql_query_execution.BaseSQLQueryExecution,
      explain: base_explain_query_plan.BaseExplainQueryPlan,
      database_information: base_database_information.BaseDatabaseInformation):
    """Initializes the SQLite Type Helper

    Args:
      execution (base_sql_query_execution.BaseSQLQueryExecution): the class
          for the execution of the SQLite queries
      explain (base_explain_query_plan.BaseExplainQueryPlan): the class for
          explain information
      database_information (base_database_information.BaseDatabaseInformation):
          the class for information about the database
    """
    super().__init__()
    self._execute = execution
    self._explain = explain
    self._information = database_information

  def GetDuplicateColumnNames(
      self, columns: sql_query_column_model.SQLColumnModel) -> [str]:
    """Find out if the query has duplicate column names and if a alias is
        needed.

    Args:
      columns (sql_query_column_model.SQLColumnModel): all columns parsed
          from the cursor
    Returns:
      [str]: a list of all the duplicate column names, if its empty it means it
          is a distinct list of columns
    """
    single_column_name_list = [column.sql_column for column in columns]
    duplicate_list = [column for column, count in
                      collections.Counter(single_column_name_list).items() if
                      count > 1]
    return sorted(duplicate_list)

  def GetColumnInformationFromDescription(
      self, descriptions: []) -> [sql_query_column_model.SQLColumnModel]:
    """Getting Information for the column out of the cursor.

    Args:
      descriptions: the descriptions of the cursor

    Returns:
      [sql_query_column_model.SQLColumnModel]: a list with all the column
          names, the types are None
    """
    sql_column = []

    if descriptions:
      sql_column = [sql_query_column_model.SQLColumnModel(
          description[0], type(None)) for description in descriptions]

    return sql_column

  def AddMissingTypesFromSchema(
      self, columns: [sql_query_column_model.SQLColumnModel], query: str,
  ) -> [sql_query_column_model.SQLColumnModel]:
    """Getting Information for the column out of the cursor.

    Args:
      columns ([sql_query_column_model.SQLColumnModel]): the columns with all
          the column names
      query: the query

    Returns:
      [sql_query_column_model.SQLColumnModel]: a list with all the columns
    """
    locked = [table.lower() for table in self._explain.GetLockedTables(query)]

    return self._ColumnTypeForMultipleTables(locked, columns, query)

  def _ColumnTypeForMultipleTables(
      self, tables: [str],
      column_model: sql_query_column_model.SQLColumnModel, query: str
  ) -> [sql_query_column_model.SQLColumnModel]:
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
    query = query.lower()

    table_and_type = {
        table: self._information.GetTableColumnsAndType(table, True) for table
        in tables}

    for column in column_model:
      column_name = column.sql_column.lower()
      # calling cell var from loop because column_name is needed multiple times
      # pylint: disable=cell-var-from-loop
      as_column_string_start = next(filter(lambda start: start > 0, map(
          lambda space: query.find(' as {0}{1}'.format(column_name, space)),
          self._POSSIBLEQUERYSEPERATOR)), None)

      # column with alias
      if as_column_string_start:
        if not self._IsPrefixedWithAlias(query, tables, column_name):
          table_end = query.rfind(' ', 0, as_column_string_start)
          table_start = table_end
        else:
          table_end = query.rfind('.', 0, as_column_string_start)
          table_start = self._GetPositionAfterSeparator(query, table_end)

        sqlite_column_name = query[table_end + 1:as_column_string_start]

      # column without alias
      else:
        if not self._IsPrefixedWithoutAlias(query, tables, column_name):
          table_end = query.rfind(' ', 0, as_column_string_start)
          table_start = table_end
        else:
          table_end = self._GetEndOfTableIfNotAlias(query, column_name)
          table_start = self._GetPositionAfterSeparator(query, table_end)
        sqlite_column_name = column_name

      table_name = query[table_start:table_end]

      # has no table prefix
      if table_name == '':
        types_sqlite = (
            [table_and_type.get(table, {}).get(sqlite_column_name, '') for table
             in tables if sqlite_column_name in table_and_type.get(table, {})])
        type_sqlite = types_sqlite[0].upper() if len(types_sqlite) else ''

      else:
        type_sqlite = table_and_type.get(
            table_name, {}).get(sqlite_column_name, '').upper()

      type_sqlite_basic = type_sqlite.split("(")[0]
      type_python = type_mapper.TypeMapperSQLitePython.MAPPINGS.get(
          type_sqlite_basic, type(None))
      column.sql_column_type = type_python

    return column_model

  def _GetEndOfTableIfNotAlias(self, query: str, column_name: str) -> bool:
    """Getting the start of the column if it is not an alias column

    Args:
      query (str): the query to be searched
      column_name (str): the name to be searched for

    Returns:
      bool: 0 if no column could be found or the starting position of the
          column
    """
    wrong_positions = [name.start() for name in
                       re.finditer('.{0} as'.format(column_name), query)]
    found_positions = []
    for space in self._POSSIBLEQUERYSEPERATOR:
      found_positions += [name.start() for name in
                          re.finditer('.{0}{1}'.format(column_name, space),
                                      query)]

    position = set(found_positions) - set(wrong_positions)

    if position:
      return position.pop()
    else:
      return 0

  def _GetPositionAfterSeparator(self, text: str, end_position: int) -> int:
    """Get the first separator position, starting at the end and searching
     in reverse

    Args:
      text (str): the text to be searched through
      end_position (int): the end position the search should be started from

    Returns:
      int: the first separator position found in the text started from the end
          position
    """
    all_appearances = [text.rfind(space, 0, end_position) for space in
                       self._POSSIBLEQUERYSEPERATOR
                       if text.rfind(space, 0, end_position) > 0]
    return max(all_appearances) + 1

  def _IsPrefixedWithAlias(self, query: str, tables: [str],
                           column_name: str) -> bool:
    """If the column has a table prefixed and has an alias

    Args:
      query (str): the query to parse
      tables ([str]): the possible tables
      column_name (str): the column name

    Returns:
      bool: True if it is prefixed, false if it isn't.
    """
    matches = [
        re.fullmatch(
            '.*({0}.)+([^ ])*( )*(as)( )*{1}( ,)*.*'.format(table, column_name),
            query)
        for table in tables if re.fullmatch(
            '.*({0}.)+([^ ])*( )*(as)( )*{1}( ,)*.*'.format(
                table, column_name), query) is not None]

    return len(matches) != 0

  def _IsPrefixedWithoutAlias(self, query: str, tables: [str],
                              column_name: str) -> bool:
    """If the column has a table prefixed and has an no alias

    Args:
      query (str): the query to parse
      tables ([str]): the possible tables
      column_name (str): the column name

    Returns:
      bool: True if it is prefixed, false if it isn't.
    """
    matches = [
        re.fullmatch(
            '.*({0}.{1})+([^ ])*( ,)*.*'.format(table, column_name), query)
        for table in tables if re.fullmatch(
            '.*({0}.{1})+([^ ])*( ,)*.*'.format(
                table, column_name), query) is not None]
    return len(matches) != 0
