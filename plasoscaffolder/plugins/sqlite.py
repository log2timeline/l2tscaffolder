# -*- coding: utf-8 -*-
"""The plugin interface classes."""
import os
import sqlite3

from plasoscaffolder.lib import definitions
from plasoscaffolder.lib import errors
from plasoscaffolder.plugins import interface
from plasoscaffolder.plugins import plaso
from plasoscaffolder.plugins import manager


class SQliteGenerator(plaso.PlasoPlugin):
  """The SQLite plugin interface."""

  # The name of the plugin or parser this scaffolder plugin provides.
  PROVIDES = 'sqlite'
  DESCRIPTION = 'Provides a plugin to generate SQLite plugins.'

  # This plugin either defines a plaso parser or a plugin.
  PLUGIN_TYPE = 'plugin'

  SCHEMA_QUERY = (
      'SELECT tbl_name, sql '
      'FROM sqlite_master '
      'WHERE type = "table" AND tbl_name != "xp_proc" '
      'AND tbl_name != "sqlite_sequence"')

  # Filename of templates.
  TEMPLATE_PARSER_FILE = 'sqlite_plugin.jinja2'
  TEMPLATE_PARSER_TEST = 'sqlite_plugin_test.jinja2'
  TEMPLATE_FORMATTER_FILE = 'sqlite_plugin_formatter.jinja2'
  TEMPLATE_FORMATTER_TEST = 'sqlite_plugin_formatter_test.jinja2'

  # Questions, a list that contains all the needed questions that the
  # user should be prompted about before the plugin or parser is created.
  # Each element in the list should be of the named tuple question.
  QUESTIONS = [
      interface.question(
          'queries', 'Query name and SQL queries to extract data',
          ('Define the name of the SQL query as well as the actual '
           'SQL queries this plugin will execute'), dict),
      interface.question(
          'required_tables', 'List of required tables',
          'Define a list of all required tables.', list)]

  def _GetSchema(self, db_path: str) -> dict:
    """Opens up a SQLite database and returns back it's schema as a dict."""
    schema = {}
    database = sqlite3.connect(db_path)
    try:
      database.row_factory = sqlite3.Row
      cursor = database.cursor()

      sql_results = cursor.execute(self.SCHEMA_QUERY)

      schema = {
          table_name: ' '.join(query.split())
          for table_name, query in sql_results}

    except sqlite3.DatabaseError as exception:
      database.close()
      raise

    return schema

  def GenerateFiles(self) -> (str, str):
    """Generate all the files required for a plaso parser or a plugin.

    Yields:
      list: file name and content of the file to be written to disk.
    """
    _, _, db_name = self._attributes.get('test_file').rpartition(os.sep)
    self._attributes['db_name'] = db_name

    sql_column_attributes = {}
    timestamp_columns = {}
    for query_name, query in self._attributes['queries'].items():
      timestamp_columns[query_name] = []
      _, _, query_string = query.lower().partition('select')
      query_attribute_string, _, _ = query_string.partition('from')
      query_attributes = query_attribute_string.split(',')
      for index, attr in enumerate(query_attributes):
        if ' AS ' in attr:
          _, _, attr = attr.partition('AS')
        elif '.' in attr:
          attr = attr.split('.')[-1]

        query_attributes[index] = attr.strip()
        if 'time' in attr:
          timestamp_columns[query_name].append(attr.strip())

      sql_column_attributes[query_name] = query_attributes

    self._attributes['query_columns'] = sql_column_attributes
    self._attributes['timestamp_columns'] = timestamp_columns

    self._attributes['db_schema'] = self._GetSchema(
        self._attributes.get('test_file'))

    return super(SQliteGenerator, self).GenerateFiles()


manager.PluginManager.RegisterPlugin(SQliteGenerator)
