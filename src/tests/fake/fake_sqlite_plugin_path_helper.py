# -*- coding: utf-8 -*-
"""Fake module containing helper functions for the SQLite plugin"""
from plasoscaffolder.bll.services import base_sqlite_plugin_path_helper


class FakeSQLitePluginPathHelper(
    base_sqlite_plugin_path_helper.BaseSQLitePluginPathHelper):
  """fake for the sqlite plugin path helper"""

  def __init__(self, unused_path: str, plugin_name: str,
               unused_database_suffix: str):
    """Initialises a fake plugin path helper

    Args:
      unused_path: the path
      plugin_name: the Name of the plugin. Will always be returned
      unused_database_suffix: the database suffix.
    """
    super().__init__()
    self.formatter_file_path = plugin_name
    self.parser_file_path = plugin_name
    self.formatter_test_file_path = plugin_name
    self.parser_test_file_path = plugin_name
    self.database_path = plugin_name
    self.parser_init_file_path = plugin_name
    self.formatter_init_file_path = plugin_name
