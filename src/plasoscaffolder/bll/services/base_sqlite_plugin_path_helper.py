# -*- coding: utf-8 -*-
"""Base class for SQLite plugin path helper."""

import abc


class BaseSQLitePluginPathHelper(object):
  """Class representing the base class for the SQLite plugin path helper.

  Attributes:
    formatter_file_path (str): the path to the formatter file
    parser_file_path (str): the path to the parser file
    formatter_test_file_path (str): the path to the formatter test file
    parser_test_file_path (str): the path to the parser test file
    database_path (str): the path to the database file
    parser_init_file_path (str): the path to the parser init file
    formatter_init_file_path (str): the path to the formatter init file
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self):
    """Initializes the SQLite plugin helper."""
    super().__init__()
    self.formatter_file_path = None
    self.parser_file_path = None
    self.formatter_test_file_path = None
    self.parser_test_file_path = None
    self.database_path = None
    self.parser_init_file_path = None
    self.formatter_init_file_path = None
