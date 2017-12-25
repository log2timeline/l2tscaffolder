# -*- coding: utf-8 -*-
# Disable linting until PyCQA/astroid/issues/362 is fixed.
# pylint: skip-file
"""SQLite plugin helper."""
import functools
import os
import re

from plasoscaffolder.bll.services import base_sqlite_plugin_helper
from plasoscaffolder.bll.services import base_sqlite_plugin_path_helper
from plasoscaffolder.dal import base_sql_query_execution
from plasoscaffolder.dal import sql_query_data
from plasoscaffolder.model import sql_query_column_model
from plasoscaffolder.model import sql_query_column_model_data
from plasoscaffolder.model import sql_query_column_model_timestamp
from plasoscaffolder.model import sql_query_model


class SQLitePluginHelper(base_sqlite_plugin_helper.BaseSQLitePluginHelper):
  """Class containing helper functions for the SQLite plugin."""

  _PLUGIN_NAME_PATTERN = re.compile("[a-z]+((_)[a-z]+)*")
  _ROW_NAME_PATTERN = re.compile("[A-Z]+([a-zA-Z])*")
  _COMMA_SEPARATED_PATTERN = re.compile("[a-zA-Z0-9]+((,)[a-zA-Z0-9]+)*")

  def __init__(self):
    """Initializes the SQLite plugin helper."""
    super().__init__()

  def PluginExists(
      self,
      path: str,
      plugin_name: str,
      database_suffix: str,
      path_helper: base_sqlite_plugin_path_helper.BaseSQLitePluginPathHelper(),
  ) -> bool:
    """Checks if the plugin already exists.

    Args:
      database_suffix: the suffix of the database file
      path (str): the path of the plaso source
      plugin_name (str): the Name of the plugin
      path_helper (BaseSQLitePluginHelper): the SQLite plugin helper

    Returns:
      bool: True if the plugin already exists. False if it does not.
    """

    helper = path_helper

    return (os.path.isfile(helper.formatter_file_path)
            or os.path.isfile(helper.parser_file_path)
            or os.path.isfile(helper.formatter_test_file_path)
            or os.path.isfile(helper.parser_test_file_path)
            or os.path.isfile(helper.database_path))

  def IsValidPluginName(self, plugin_name: str) -> bool:
    """Validates the plugin name.

    Args:
      plugin_name (str): the plugin name

    Returns:
      bool: true if the plugin name is valid
    """
    return self._PLUGIN_NAME_PATTERN.fullmatch(plugin_name)

  def IsValidRowName(self, row_name: str) -> bool:
    """Validates the row name.

    Args:
      row_name (str): the row name

    Returns:
      bool: true if the row name is valid
    """
    return self._ROW_NAME_PATTERN.fullmatch(row_name)

  def IsValidCommaSeparatedString(self, text: str) -> bool:
    """Validates a comma separated string

    Args:
      text (str): the string to validate

    Returns:
      bool: true if the text is valid
    """
    return self._COMMA_SEPARATED_PATTERN.fullmatch(text)

  def FileExists(self, path: str) -> bool:
    """Checks if the file exists.

    Args:
      path: the plaso folder path

    Returns: true if the file exists
    """
    return os.path.isfile(path)

  def FolderExists(self, path: str) -> bool:
    """Checks if folder exists.

    Args:
      path: the plaso folder path

    Returns: true if the folder exists
    """
    return os.path.isdir(path)

  def RunSQLQuery(
      self, query: str,
      executor: base_sql_query_execution.BaseSQLQueryExecution
  ) -> sql_query_data.SQLQueryData:
    """Validates the SQL query.

    Args:
      executor (base_sql_query_execution.SQLQueryExection()) the SQL executor
      query (str): the SQL query

    Returns:
      sql_query_data.SQLQueryData: data returned by executing the
          query
    """
    return executor.ExecuteReadOnlyQuery(query)

  def GetDistinctColumnsFromSQLQueryData(
      self,
      queries: [sql_query_model.SQLQueryModel]) -> [str]:
    """Get a distinct list of all attributes from multiple queries.

    Args:
      queries ([sql_query_model.SQLQueryModel]): an array of multiple
          SQL query data objects

    Returns:
      list[str]: all distinct attributes used in the query
    """
    if len(queries) != 0:
      list_of_list_of_column_model = [query.columns for query in queries]
      list_of_column_model = functools.reduce(lambda x, y: x + y,
                                              list_of_list_of_column_model)
      list_of_columns_snake_case = [column.GetColumnAsSnakeCase() for column in
                                    list_of_column_model]
      distinct_columns = sorted(set().union(list_of_columns_snake_case))
      return distinct_columns
    else:
      return []

  def GetAssumedTimestamps(
      self, columns: [sql_query_column_model.SQLColumnModel]) -> [str]:
    """Gets all columns assumed that they are timestamps

    Args:
      columns ([sql_query_column_model.SQLColumnModel]): the columns from the
          SQL query

    Returns:
      [str]: the names from the columns assumed they could be a timestamp
    """
    assumed_columns = [column.sql_column for column in columns
                       if 'time' in column.sql_column.lower() or 'date' in
                       column.sql_column.lower()]
    return assumed_columns

  def GetColumnsAndTimestampColumn(
      self, columns: [sql_query_column_model.SQLColumnModel],
      timestamps: [str], data: [str]
  ) -> (
      [sql_query_column_model_data.SQLColumnModelData],
      [sql_query_column_model_timestamp.SQLColumnModelTimestamp]):
    """Splits the column list into a list of simple columns and a list for
    timestamp event columns and adds the data to the simple columns

    Args:
      columns ([sql_query_column_model_data.SQLColumnModelData]): the columns
          from the SQL query
      timestamps ([str]): the timestamp events
      data ([str]): the data from the cursor

    Returns:
      ([sql_query_column_model_data.SQLColumnModelData],
          [sql_query_column_model_timestamp.SQLColumnModelTimestamp]): a tuple
          of columns, the first are the normal columns, the second are the 
          timestamp events
    """
    normal_columns = list()
    message = {}
    timestamps_data = {}

    timestamp_columns = self._GetTimestampColumnsFromColumnsWithoutMessage(
        columns, timestamps)

    for column_index in range(0, len(columns)):
      column = columns[column_index]
      data_row = 0

      if column.sql_column in timestamps:
        data_row = [timestamp.sql_column for timestamp in
                    timestamp_columns].index(column.sql_column)
        timestamps_data[column.sql_column] = self._GetDataForTimestamp(
            data, data_row, column_index)
        data_row += 1
      else:
        column_data_model, message = self._GetDataForColumnAndAppendMessage(
            data, column,
            timestamp_columns, column_index, message)

        normal_columns.append(column_data_model)

    timestamp_columns = self._AddMessageAndDataToTimestampColumns(
        timestamp_columns, message, timestamps_data)

    return normal_columns, timestamp_columns

  def _AddMessageAndDataToTimestampColumns(
      self, timestamp_columns: [
        sql_query_column_model_timestamp.SQLColumnModelTimestamp],
      message: {str, str}, timestamps_data: {str, str}
  ) -> [sql_query_column_model_timestamp.SQLColumnModelTimestamp]:
    """Add Missing Message and data to the timestamp columns

    Args:
      timestamp_columns ([
          sql_query_column_model_timestamp.SQLColumnModelTimestamp]): the
          columns to be changed
      message {str_str}: The message to be added.Dictionary with first
          part the timestamp name as key and second the message
      timestamps_data {str,str}: The data to be added. Dictionary with first
          part the timestamp name as key and second the data

    Returns:
      [sql_query_column_model_timestamp.SQLColumnModelTimestamp]: the timestamp
          columns with additional data and message
    """
    for timestamp in timestamp_columns:
      timestamp.expected_message = message[timestamp.sql_column]
      timestamp.timestamp = timestamps_data[timestamp.sql_column]
    return timestamp_columns

  def _GetDataForColumnAndAppendMessage(
      self, data: [str], column: sql_query_column_model_data.SQLColumnModelData,
      timestamp_columns: [
        sql_query_column_model_timestamp.SQLColumnModelTimestamp],
      column_index: int, message: {str, str}
  ) -> (sql_query_column_model_data.SQLColumnModelData, {str, str}):
    """Get the data for the column and append data to the message for the
    timestamp message.

    Args:
      data ([str]): the data to the query.
      column (sql_query_column_model_data.SQLColumnModelData): the column to
          get the data for
      timestamp_columns ([
          sql_query_column_model_timestamp.SQLColumnModelTimestamp]): the
              timestamp columns to get data for each timestamp
      column_index (int): the index of the column in the data
      message ({str,str}): the existing message for the timestamp to append the
          new content

    Returns:
       sql_query_column_model_data.SQLColumnModelData, {str, str}: the data
           model for the column and the passed message with the appended data
    """
    column_data = {}
    data_row = 0
    for timestamp in [timestamp.sql_column for timestamp in
                      timestamp_columns]:

      data_for_column_and_timestamp = ''
      if data:
        data_for_column_and_timestamp = data[data_row][column_index]
        # if not enough data results it shall take the same data as before
        if data_row < len(data) - 1:
          data_row += 1

      column_data[timestamp] = data_for_column_and_timestamp

      message = self._GetTimestampMessageWithAddedColumnData(
          timestamp, message, column.GetColumnAsDescription(),
          data_for_column_and_timestamp)

    column_data_model = sql_query_column_model_data.SQLColumnModelData(
        sql_column=column.sql_column,
        sql_column_type=column.sql_column_type,
        data=column_data)

    return column_data_model, message

  def _GetTimestampMessageWithAddedColumnData(
      self, timestamp: str, message: {str: str}, description: str,
      data: str) -> {str: str}:
    """Append Data to the given message for a timestamp

    Args:
      timestamp (str): the timestamp to append data to
      message ({str:str}): the message to be changed
      description (str): the description to be added for the timestamp
      data (str): the data to be added for the timestamp

    Returns:
      {str:str}: the given message with new data added for the given timestamp
    """
    if timestamp not in message:
      message[timestamp] = '{0}: {1}'.format(description, data)
    else:
      message[timestamp] = '{0} {1}: {2}'.format(
          message[timestamp], description, data)

    return message

  def _GetDataForTimestamp(self, data: [str], data_row: int,
                           timestamp_index: int):
    """Get the data for the timestamp out of the data array

    Args:
      data ([str]): the data array
      data_row (int): the data row from the data array to get the data from
      timestamp_index (int): the index in the data row where the data for the
        timestamp is located

    Returns:
      str: the data for the timestamp
    """
    timestamp_data = ''
    if data:
      if len(data) > data_row:
        timestamp_data = data[data_row][timestamp_index]
      else:
        timestamp_data = data[len(data) - 1][timestamp_index]

    return timestamp_data

  def _GetTimestampColumnsFromColumnsWithoutMessage(
      self, columns: [sql_query_column_model.SQLColumnModel],
      timestamps: [str]
  ) -> [sql_query_column_model_timestamp.SQLColumnModelTimestamp]:
    """Gets the timestamp columns from the columns and sets the type and the
    name but not the message.

    Args:
    columns ([sql_query_column_model_data.SQLColumnModelData]): the columns
          from the SQL query
      timestamps ([str]): the timestamp events

    Returns:
      [sql_query_column_model_data.SQLColumnModelData]: the timestamp columns
          but without the message
    """
    timestamp_columns = list()
    for column in [column for column in columns if
                   column.sql_column in timestamps]:
      timestamp_data_model = (
        sql_query_column_model_timestamp.SQLColumnModelTimestamp(
            sql_column_type=column.sql_column_type,
            sql_column=column.sql_column,
            expected_message=''))
      timestamp_columns.append(timestamp_data_model)
    return timestamp_columns
