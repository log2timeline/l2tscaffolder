# -*- coding: utf-8 -*-
"""The scaffolder interface classes."""
import os
import sqlite3

from typing import Iterator
from typing import Tuple

from plasoscaffolder.scaffolders import interface
from plasoscaffolder.scaffolders import plaso
from plasoscaffolder.scaffolders import manager


class PlasoSQLiteScaffolder(plaso.PlasoPluginScaffolder):
  """The plaso SQLite plugin scaffolder."""

  # The name of the plugin or parser this scaffolder provides.
  NAME = 'sqlite'
  DESCRIPTION = 'Provides a scaffolder to generate a plaso SQLite plugin.'

  SCHEMA_QUERY = (
      'SELECT tbl_name, sql '
      'FROM sqlite_master '
      'WHERE type = "table" AND tbl_name != "xp_proc" '
      'AND tbl_name != "sqlite_sequence"')

  # Filenames of templates.
  TEMPLATE_PARSER_FILE = 'sqlite_plugin.jinja2'
  TEMPLATE_PARSER_TEST = 'sqlite_plugin_test.jinja2'
  TEMPLATE_FORMATTER_FILE = 'sqlite_plugin_formatter.jinja2'
  TEMPLATE_FORMATTER_TEST = 'sqlite_plugin_formatter_test.jinja2'

  # Questions, a list that contains all the needed questions that the
  # user should be prompted about before the plugin or parser is created.
  # Each element in the list should be of the named tuple question.
  QUESTIONS = [
      interface.Question(
          'queries', 'Query name and SQL queries to extract data',
          ('Define the name of the SQL query as well as the actual '
           'SQL queries this plugin will execute'), dict),
      interface.Question(
          'required_tables', 'List of required tables',
          'Define a list of all required tables.', list)]

  def _GetQueryAttributes(self, query: str) -> Iterator[str]:
    """Generates attributes extracted from the FROM statement of a SQL query.

    Args:
      query (str): a SQL query.

    Yields:
      str: an attribute extracted from the FROM statement of a SQL query.
    """
    _, _, query_string = query.lower().partition('select')
    query_attribute_string, _, _ = query_string.partition('from')

    for attribute in query_attribute_string.split(','):
      if ' as ' in attribute.lower():
        _, _, attribute = attribute.lower().partition(' as ')
      elif '.' in attribute:
        attribute = attribute.split('.')[-1]

      yield attribute.strip()

  def _GetSchema(self, database_path: str) -> dict:
    """Returns the schema of a SQLite database as a dict.

    Args:
      database_path (str): full path to the SQLite database.

    Returns:
      (dict): where keys are the name of each defined table in the
          database and the value is the SQL command that was used to
          create the table.
    """
    schema = {}
    database = sqlite3.connect(database_path)
    try:
      database.row_factory = sqlite3.Row
      cursor = database.cursor()

      sql_results = cursor.execute(self.SCHEMA_QUERY)

      schema = {
          table_name: ' '.join(query.split())
          for table_name, query in sql_results}

    except sqlite3.DatabaseError:
      database.close()
      raise

    return schema

  def GenerateFiles(self) -> Iterator[Tuple[str, str]]:
    """Generates all the files required for the SQLite plugin.

    Yields:
      tuple (str, str): file name and content of the file to be written to disk.
    """
    _, _, database_name = self._attributes.get('test_file').rpartition(os.sep)
    self._attributes['database_name'] = database_name

    self._attributes['data_types'] = {}
    sql_column_attributes = {}
    timestamp_columns = {}

    for query_name, query in self._attributes['queries'].items():
      self._attributes['data_types'][query_name] = '{0:s}:{1:s}'.format(
          self._output_name.lower().replace('_', ':'), query_name.lower())
      timestamp_columns[query_name] = []
      sql_column_attributes[query_name] = []

      for attribute in self._GetQueryAttributes(query):
        if 'time' in attribute:
          timestamp_columns[query_name].append(attribute.strip())
        sql_column_attributes[query_name].append(attribute)

    self._attributes['query_columns'] = sql_column_attributes
    self._attributes['timestamp_columns'] = timestamp_columns

    self._attributes['database_schema'] = self._GetSchema(
        self._attributes.get('test_file'))

    return super(PlasoSQLiteScaffolder, self).GenerateFiles()


manager.ScaffolderManager.RegisterScaffolder(PlasoSQLiteScaffolder)
