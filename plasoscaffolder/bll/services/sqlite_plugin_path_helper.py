# -*- coding: utf-8 -*-
"""SQLite Plugin Path Helper-"""
import os

from plasoscaffolder.bll.services import base_sqlite_plugin_path_helper


class SQLitePluginPathHelper(
    base_sqlite_plugin_path_helper.BaseSQLitePluginPathHelper):
  """Class containing helper functions for the SQLite plugin for the path-

  Attributes:
    formatter_file_path (str): the path to the formatter file
    parser_file_path (str): the path to the parser file
    formatter_test_file_path (str): the path to the formatter test file
    parser_test_file_path (str): the path to the parser test file
    database_path (str): the path to the database file
    parser_init_file_path (str): the path to the parser init file
    formatter_init_file_path (str): the path to the formatter init file
  """

  def __init__(self, path: str, plugin_name: str, database_suffix: str):
    """Initializes the SQLite plugin helper.

      Args:
       path (str): the plaso folder path
       plugin_name (str): The Name of the plugin to check.
       database_suffix (str): the file suffix of the database file
     """
    super().__init__()
    file_name = '{0:s}.py'.format(plugin_name)
    database_name = '{0:s}.{1:s}'.format(plugin_name, database_suffix)

    self.formatter_file_path = os.path.join(
        path, 'plaso', 'formatters', file_name)
    self.parser_file_path = os.path.join(
        path, 'plaso', 'parsers', 'sqlite_plugins', file_name)
    self.formatter_test_file_path = os.path.join(
        path, 'tests', 'formatters', file_name)
    self.parser_test_file_path = os.path.join(
        path, 'tests', 'parsers', 'sqlite_plugins', file_name)
    self.database_path = os.path.join(path, 'test_data', database_name)
    self.parser_init_file_path = os.path.join(
        path, 'plaso', 'parsers', 'sqlite_plugins', '__init__.py')
    self.formatter_init_file_path = os.path.join(
        path, 'plaso', 'formatters', '__init__.py')
