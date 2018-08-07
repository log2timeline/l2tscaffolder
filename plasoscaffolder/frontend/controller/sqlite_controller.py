# -*- coding: utf-8 -*-
"""File representing the Controller for SQLite plugin."""
import os

import click
from plasoscaffolder.bll.mappings import formatter_init_mapping
from plasoscaffolder.bll.mappings import formatter_mapping
from plasoscaffolder.bll.mappings import formatter_test_mapping
from plasoscaffolder.bll.mappings import mapping_helper
from plasoscaffolder.bll.mappings import parser_init_mapping
from plasoscaffolder.bll.mappings import parser_mapping
from plasoscaffolder.bll.mappings import parser_test_mapping
from plasoscaffolder.bll.services import base_sqlite_plugin_helper
from plasoscaffolder.bll.services import sqlite_generator
from plasoscaffolder.bll.services import sqlite_plugin_helper
from plasoscaffolder.bll.services import sqlite_plugin_path_helper
from plasoscaffolder.common import base_output_handler
from plasoscaffolder.common import file_handler
from plasoscaffolder.dal import base_sql_query_execution
from plasoscaffolder.dal import explain_query_plan
from plasoscaffolder.dal import sqlite_database_information
from plasoscaffolder.dal import sqlite_query_execution
from plasoscaffolder.model import sql_query_column_model
from plasoscaffolder.model import sql_query_column_model_data
from plasoscaffolder.model import sql_query_column_model_timestamp
from plasoscaffolder.model import sql_query_model


class SQLiteController(object):
  """Class representing the SQLite Controller."""

  _NUMBER_OF_SQLITE_OUTPUT_EXAMPLES = 3

  def __init__(self, output_handler: base_output_handler.BaseOutputHandler(),
               plugin_helper:
               base_sqlite_plugin_helper.BaseSQLitePluginHelper()):
    """Initializes the SQLite Controller.

    Args:
      output_handler (base_output_handler.BaseOutputHandler): the handler for
          the output
      plugin_helper (base_sqlite_plugin_helper.BaseSQLitePluginHelper): the
          helper for the SQLite plugin
    """
    super(SQLiteController, self).__init__()
    self._path = None
    self._name = None
    self._testfile = None
    self._sql_query = []
    self._plugin_helper = plugin_helper
    self._output_handler = output_handler
    self._query_execution = None

  def SourcePath(self, unused_ctx: click.core.Context,
                 unused_param: click.core.Option,
                 value: str) -> str:
    """Saving the source path.

    Args:
      unused_ctx (click.core.Context): the click context (automatically given
        via callback)
      unused_param (click.core.Option): the click command (automatically
        given via callback)
      value (str): the source path (automatically given via callback)

    Returns:
      str: the source path representing the same as value
    """
    while not self._plugin_helper.FolderExists(value):
      value = self._output_handler.PromptError(
          'Folder does not exists. Enter correct one')
    self._path = value
    return value

  def PluginName(self, unused_ctx: click.core.Context,
                 unused_param: click.core.Option,
                 value: str) -> str:
    """Saving the plugin name.

    Args:
      unused_ctx (click.core.Context): the click context (automatically given
          via callback)
      unused_param (click.core.Option): the click command (automatically
          given via callback)
      value (str): the source path (automatically given via callback)

    Returns:
      str: the plugin name representing the same as value
    """
    value = self._ValidatePluginName(value)
    while self._plugin_helper.PluginExists(
        self._path, value, '',
        sqlite_plugin_path_helper.SQLitePluginPathHelper(
            self._path, value, '')):
      value = self._output_handler.PromptError(
          'Plugin exists. Choose new Name')
      value = self._ValidatePluginName(value)

    self._name = value
    return value

  def TestPath(self, unused_ctx: click.core.Context,
               unused_param: click.core.Option,
               value: str) -> str:
    """Saving the path to the test file.

    Args:
      unused_ctx (click.core.Context): the click context (automatically given
          via callback)
      unused_param (click.core.Option): the click command (automatically
          given via callback)
      value (str): the source path (automatically given via callback)

    Returns:
      str: the test file path representing the same as the value
    """
    no_database_file = True

    while no_database_file:
      while not self._plugin_helper.FileExists(value):
        value = self._output_handler.PromptError(
            'File does not exists. Choose another.')
      if not self._IsDatabaseFile(value):
        value = self._output_handler.PromptError(
            'Unable to open the database file. Choose another.')
      else:
        no_database_file = False

    self._testfile = value
    return value

  def _IsDatabaseFile(self, path: str) -> bool:
    """Try to open the database File.

    Args:
      path (str): the database file path

    Returns:
      bool: if the file can be opened and is a database file
    """
    execution = sqlite_query_execution.SQLiteQueryExecution(path)
    if execution.TryToConnect():
      self._query_execution = execution
      return True
    return False

  def SQLQuery(self, unused_ctx: click.core.Context,
               unused_param: click.core.Option,
               value: str) -> [sql_query_model.SQLQueryModel]:
    """The SQL Query of the plugin.

    Args:
      unused_ctx (click.core.Context): the click context (automatically given
          via callback)
      unused_param (click.core.Option): the click command (automatically
          given via callback)
      value (str): the SQL Query (automatically given via callback)

    Returns:
      [sql_query_model.SQLQueryModel]: a list of SQL Query models
    """
    verbose = value
    add_more_queries = True
    sql_query_list = []
    while add_more_queries:
      if len(sql_query_list) > 0:
        sql_query = self._output_handler.PromptInfo(
            text='Please write your SQL script for the plugin [\'abort\' to '
                 'continue]')
        if sql_query == 'abort':
          add_more_queries = False
      else:
        sql_query = self._output_handler.PromptInfo(
            text='Please write your SQL script for the plugin')
      if add_more_queries:
        query_model = self._CreateSQLQueryModelWithUserInput(
            sql_query, verbose, self._query_execution)
        if query_model is not None:
          sql_query_list.append(query_model)
          add_more_queries = self._output_handler.Confirm(
              text='Do you want to add another Query?',
              abort=False, default=True)

    self._sql_query = sql_query_list
    return sql_query_list

  def _CreateSQLQueryModelWithUserInput(
      self,
      query: str, with_examples: bool,
      query_execution: base_sql_query_execution.BaseSQLQueryExecution()
  ) -> sql_query_model.SQLQueryModel:
    """Asks the user information about the SQL Query.

    Args:
      query (str): the SQL Query
      with_examples (bool): if the user wants examples for the given Query

    Returns:
      sql_query_model.SQLQueryModel: a SQL Query model
    """
    query_data = self._plugin_helper.RunSQLQuery(query, query_execution)
    query_plan = explain_query_plan.ExplainQueryPlan(query_execution)

    if query_data.has_error:
      self._output_handler.PrintError(str(query_data.error_message))
      return None

    else:
      if with_examples:
        length = len(query_data.data)
        if length == 0:
          self._output_handler.PrintInfo('Your query does not return anything.')
        else:
          self._output_handler.PrintInfo(
              'Your query output could look like this.')
          self._output_handler.PrintInfo(
              str(list(map(lambda x: x.sql_column, query_data.columns))))
          amount = min(self._NUMBER_OF_SQLITE_OUTPUT_EXAMPLES, length)
          for index in range(0, amount):
            self._output_handler.PrintInfo(str(query_data.data[index]))

        add_query = self._output_handler.Confirm(
            'Do you want to add this query?',
            abort=False, default=True)
        if not add_query:
          return None
      else:
        self._output_handler.PrintError('The SQL query was ok.')

      locked_tables = query_plan.GetLockedTables(query)
      name = ''.join(locked_tables).capitalize()

      question_parse = 'Do you want to name the query parse row: {0} ?'.format(
          name)
      add_recommended_name = self._output_handler.Confirm(
          question_parse, abort=False, default=True)

      if not add_recommended_name:
        question_event = 'What row does the SQL Query parse?'
        initial_name = self._output_handler.PromptInfo(question_event)
        name = self._ValidateRowName(initial_name)

      data_column, timestamp_column = self.GetTimestamps(
          query_data.columns, query_data.data)

      if query_data.data is not None:
        amount_events = len(query_data.data)
      else:
        amount_events = 0

      message = 'Does the event {0} need customizing?'.format(name)
      needs_customizing = self._output_handler.Confirm(
          text=message, abort=False, default=False)
      if needs_customizing:
        data_column = self.GetCustomizable(data_column)

    return sql_query_model.SQLQueryModel(
        query.strip(), name, data_column, timestamp_column, needs_customizing,
        amount_events)

  def GetTimestamps(
      self, columns: [sql_query_column_model.SQLColumnModel], data: [str]
  ) -> ([sql_query_column_model_data.SQLColumnModelData],
        [sql_query_column_model_timestamp.SQLColumnModelTimestamp]):
    """Gets the timestamp from the user and the columns.

    Args:
      columns ([sql_query_column_model.SQLColumnModel]): the columns from the
          SQL query.
      data ([str]): the data from the cursor

    Returns:
       [sql_query_column_model_data.SQLColumnModelData],
           [sql_query_column_model_timestamp.SQLColumnModelTimestamp]: A
           tuple of columns. The first column represents the
           normal column for the query. The second
           column represents the timestamp events.
    """
    timestamps = set()
    wrong_timestamps = set()

    assumed_timestamps = self._plugin_helper.GetAssumedTimestamps(columns)
    for timestamp in assumed_timestamps:
      question_timestamp = 'Is the column a time event? {0}'.format(timestamp)
      is_timestamp = self._output_handler.Confirm(question_timestamp,
                                                  abort=False, default=True)
      if is_timestamp:
        timestamps.add(timestamp)

    add_own_timestamps = True
    while add_own_timestamps:
      own_timestamps = self._output_handler.PromptInfo(
          'Enter (additional) timestamp events from the query [columnName,'
          'aliasName...] or [abort]')
      if own_timestamps == 'abort':
        add_own_timestamps = False
      else:
        if len(timestamps) == 0:
          own_timestamps = self._output_handler.PromptInfo(
              'At least one timestamp is required, please add a timestamp')
        own_timestamps = self._ValidateTimestampString(own_timestamps)

        new_columns = self._GetValidColumnsAndInvalid(columns, own_timestamps)
        timestamps.update(new_columns[0])
        wrong_timestamps.update(new_columns[1])

        self._PrintAddedAndFailedColumns(timestamps, wrong_timestamps)
        add_own_timestamps = self._output_handler.Confirm(
            'Do you want to add more timestamps?', abort=False, default=False)

    return self._plugin_helper.GetColumnsAndTimestampColumn(
        columns, timestamps, data)

  def GetCustomizable(
      self, columns: [sql_query_column_model_data.SQLColumnModelData]
  ) -> [sql_query_column_model_data.SQLColumnModelData]:
    """Gets the customizable columns from the user

    Args:
      columns ([sql_query_column_model_data.SQLColumnModelData]): the columns
          from the SQL query.

    Returns:
     [sql_query_column_model_data.SQLColumnModelData]: the columns
          from the SQL query an set if the column is customizable
    """
    customizable = set()
    wrong_customizable = set()

    add_own_customizable = True
    while add_own_customizable:
      own_column = self._output_handler.PromptInfo(
          'Enter columns that are customizable [columnName,aliasName...] or '
          '[abort]')
      own_column = self._ValidateColumnString(own_column)

      if own_column == 'abort':
        if len(customizable) == 0:
          own_column = self._output_handler.PromptInfo(
              'At least one column is required, please add a column')
          own_column = self._ValidateColumnString(own_column)
        else:
          add_own_customizable = False

      if add_own_customizable:
        new_columns = self._GetValidColumnsAndInvalid(columns, own_column)
        customizable.update(new_columns[0])
        wrong_customizable.update(new_columns[1])

        self._PrintAddedAndFailedColumns(customizable, wrong_customizable)
        add_own_customizable = self._output_handler.Confirm(
            'Do you want to add more columns that are customizable?',
            abort=False, default=False)

    for column in columns:
      if column.sql_column in customizable:
        column.customize = True

    return columns

  def Generate(self, template_path: str, yapf_path: str):
    """Generating the files.

    Args:
      template_path (str): the path to the template directory
      yapf_path (str): the path to the yapf style file
    """
    self._output_handler.Confirm('Do you want to Generate the files?')

    database_suffix = os.path.splitext(self._testfile)[1][1:]
    sqlite_mapping_helper = mapping_helper.MappingHelper(
        template_path, yapf_path)

    generator = sqlite_generator.SQLiteGenerator(
        self._path,
        self._name,
        self._testfile,
        self._sql_query,
        self._output_handler,
        sqlite_plugin_helper.SQLitePluginHelper(),
        sqlite_plugin_path_helper.SQLitePluginPathHelper(
            self._path, self._name, database_suffix))

    generator.GenerateSQLitePlugin(
        template_path, file_handler.FileHandler(),
        formatter_init_mapping.FormatterInitMapping(sqlite_mapping_helper),
        parser_init_mapping.ParserInitMapping(sqlite_mapping_helper),
        parser_mapping.ParserMapper(sqlite_mapping_helper),
        formatter_mapping.FormatterMapper(sqlite_mapping_helper),
        parser_test_mapping.ParserTestMapper(sqlite_mapping_helper),
        formatter_test_mapping.FormatterTestMapper(sqlite_mapping_helper),
        sqlite_mapping_helper,
        sqlite_database_information.SQLiteDatabaseInformation(
            self._query_execution))

  def _ValidatePluginName(self, plugin_name: str) -> str:
    """Validate plugin name and prompt until name is valid.

    Args:
      plugin_name (str): the name of the plugin

    Returns:
      str: a valid plugin name
    """
    while not self._plugin_helper.IsValidPluginName(plugin_name):
      plugin_name = self._output_handler.PromptError(
          'Plugin is not in a valid format. Choose new Name ['
          'plugin_name_...]')
    return plugin_name

  def _ValidateRowName(self, row_name: str) -> str:
    """Validate row name and prompt until name is valid.

    Args:
      row_name (str): the name of the row

    Returns:
      str: a valid row name
    """
    while not self._plugin_helper.IsValidRowName(row_name):
      row_name = self._output_handler.PromptError(
          'Row name is not in a valid format. Choose new Name [RowName...]')
    return row_name

  def _ValidateTimestampString(self, timestamp_string: str) -> str:
    """Validate the timestamp string and prompt until valid

    Args:
      timestamp_string (str): the string with the timestamps

    Returns:
      str: a comma separated string with timestamps
    """
    while not self._plugin_helper.IsValidCommaSeparatedString(timestamp_string):
      timestamp_string = self._output_handler.PromptError(
          'Timestamps are not in valid format. Reenter them correctly [name,'
          'name...]')
    return timestamp_string

  def _ValidateColumnString(self, column_string: str) -> str:
    """Validate the timestamp string and prompt until valid

    Args:
      column_string (str): the string with the column names

    Returns:
      str: a comma separated string with column names
    """
    while not self._plugin_helper.IsValidCommaSeparatedString(column_string):
      column_string = self._output_handler.PromptError(
          'Column names are not in valid format. Reenter them correctly [name,'
          'name...]')
    return column_string

  def _PrintAddedAndFailedColumns(self, added: [str], failed: [str]):
    """Prints the user which columns failed and which are added

    Args:
      added ([str]): the added columns
      failed ([str]): the failed columns
    """
    added_string = 'Added: {0}'.format(','.join(sorted(added)))
    failed_string = 'Failed: {0}'.format(','.join(sorted(failed)))
    self._output_handler.PrintInfo(added_string)
    self._output_handler.PrintInfo(failed_string)

  def _GetValidColumnsAndInvalid(
      self, columns: [sql_query_column_model.SQLColumnModel], user_input: str
  ) -> ([str], [str]):
    """

    Args:
      columns ([sql_query_column_model.SQLColumnModel]): the columns from the
          SQL query.
      user_input: a comma separated list of column names

    Returns:
      [str], [str]: the columns for the right column names and the wrong
          column names as the second part of the tuple
    """
    right_columns = set()
    wrong_columns = set()
    for column in user_input.split(','):
      column_names = [column.sql_column for column in columns]
      if column in column_names:
        right_columns.add(column)
      else:
        wrong_columns.add(column)
    return right_columns, wrong_columns
