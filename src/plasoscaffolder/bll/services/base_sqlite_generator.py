# -*- coding: utf-8 -*-
"""Base class for a Generator for SQLite."""
import abc
import os

from plasoscaffolder.bll.mappings import base_sqliteplugin_mapping
from plasoscaffolder.bll.mappings import base_mapping_helper
from plasoscaffolder.common import base_file_handler
from plasoscaffolder.dal import base_database_information


class BaseSQLiteGenerator(object):
  """Class representing the base class for the base SQLite generator."""
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def GenerateSQLitePlugin(
      self,
      template_path: str,
      fileHandler: base_file_handler.BaseFileHandler,
      formatter_init_mapper: base_sqliteplugin_mapping.BaseSQLitePluginMapper,
      parser_init_mapper: base_sqliteplugin_mapping.BaseSQLitePluginMapper,
      parser_mapper: base_sqliteplugin_mapping.BaseSQLitePluginMapper,
      formatter_mapper: base_sqliteplugin_mapping.BaseSQLitePluginMapper,
      parser_test_mapper: base_sqliteplugin_mapping.BaseSQLitePluginMapper,
      formatter_test_mapper: base_sqliteplugin_mapping.BaseSQLitePluginMapper,
      mappingHelper: base_mapping_helper.BaseMappingHelper,
      database_information: base_database_information.BaseDatabaseInformation):
    """Generate the whole SQLite plugin.

    Args:
      template_path (str): the path to the template directory
      fileHandler (base_file_handler.BaseFileHandler): the handler for the file
      formatter_init_mapper (base_sqliteplugin_mapping.BaseSQLitePluginMapper):
          the init formatter mapper
      parser_init_mapper (base_sqliteplugin_mapping.BaseSQLitePluginMapper):
          the init parser mapper
      parser_mapper (base_sqliteplugin_mapping.BaseSQLitePluginMapper):
          the parser mapper
      formatter_mapper (base_sqliteplugin_mapping.BaseSQLitePluginMapper):
          the mapper for the formatter
      parser_test_mapper (base_sqliteplugin_mapping.BaseSQLitePluginMapper):
          the mapper for the formatter test
      formatter_test_mapper (base_sqliteplugin_mapping.BaseSQLitePluginMapper):
          the mapper for the parser test
      mappingHelper (base_mapping_helper.BaseMappingHelper): the mapping helper
      database_information (base_database_information.BaseDatabaseInformation):
          helper class for information about the database
    """

  @abc.abstractmethod
  def _Print(self, formatter: str, parser: str, formatter_test: str,
             parser_test: str, database: str, parser_init: str,
             formatter_init: str):
    """Printing the information to the generated files.

    Args:
      formatter (str): the formatter file
      parser(str): the parser file
      formatter_test(str): the formatter test file
      parser_test(str): the parser test file
      database(str): the database file
      parser_init(str): the parser init file
      formatter_init(str): the formatter init file
    """

  @abc.abstractmethod
  def _PrintCopy(self, file: str):
    """Print for copy file.

    Args:
      file (str): the file path
    """

  @abc.abstractmethod
  def _PrintEdit(self, file: str):
    """Print for edit file.

    Args:
      file (str): the file path
    """

  @abc.abstractmethod
  def _PrintCreate(self, file: os.path):
    """Print for create file.

    Args:
      file (str): the file path
    """
