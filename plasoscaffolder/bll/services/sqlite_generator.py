# -*- coding: utf-8 -*-
"""A SQLite Generator"""
import os

from plasoscaffolder.bll.mappings import base_mapping_helper
from plasoscaffolder.bll.mappings import base_sqliteplugin_mapping
from plasoscaffolder.bll.services import base_sqlite_generator
from plasoscaffolder.bll.services import base_sqlite_plugin_helper
from plasoscaffolder.bll.services import base_sqlite_plugin_path_helper
from plasoscaffolder.common import base_file_handler
from plasoscaffolder.common import base_output_handler
from plasoscaffolder.dal import base_database_information
from plasoscaffolder.model import formatter_data_model, init_data_model
from plasoscaffolder.model import formatter_test_data_model
from plasoscaffolder.model import parser_data_model
from plasoscaffolder.model import parser_test_data_model
from plasoscaffolder.model import sql_query_model


class SQLiteGenerator(base_sqlite_generator.BaseSQLiteGenerator):
  """Generator for SQLite Files."""

  def __init__(
      self, path: str, name: str, database: str,
      queries: [sql_query_model.SQLQueryModel],
      output_handler: base_output_handler.BaseOutputHandler,
      pluginHelper: base_sqlite_plugin_helper.BaseSQLitePluginHelper,
      pathHelper: base_sqlite_plugin_path_helper.BaseSQLitePluginPathHelper
  ):
    """Initializes a SQLite Generator.

    Args:
      path (str): the path of the plaso folder
      name (str): the Name of the plugin
      database (str): the path to the database
      queries ([sql_query_model.SQLQueryModel]): list of queries
      output_handler (base_output_handler.BaseOutputHandler): the output
          handler for the generation information
      pluginHelper (base_sqlite_plugin_helper.BaseSQLitePluginHelper): the
          plugin helper
      pathHelper (base_sqlite_plugin_path_helper.BaseSQLitePluginPathHelper):
          the plugin path helper
    """
    super().__init__()

    self.queries = queries
    self.path = path
    self.name = name
    self.database = database

    self.path_helper = pathHelper
    self.output = output_handler
    self.plugin_helper = pluginHelper

    self.init_formatter_exists = self.plugin_helper.FileExists(
        self.path_helper.formatter_init_file_path)
    self.init_parser_exists = self.plugin_helper.FileExists(
        self.path_helper.parser_init_file_path)

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
    file_handler = fileHandler

    parser_data = parser_data_model.ParserDataModel(
        database_name=os.path.basename(self.path_helper.database_path),
        queries=self.queries,
        plugin_name=self.name,
        required_tables=database_information.GetTablesFromDatabase())

    formatter_data = formatter_data_model.FormatterDataModel(
        queries=self.queries,
        plugin_name=self.name)

    parser_test_data = parser_test_data_model.ParserTestDataModel(
        database_name=os.path.basename(self.path_helper.database_path),
        queries=self.queries,
        plugin_name=self.name
    )

    formatter_test_data = formatter_test_data_model.FormatterTestDataModel(
        queries=self.queries,
        plugin_name=self.name
    )

    parser_init_data = init_data_model.InitDataModel(
        plugin_name=self.name,
        is_create_template=not self.init_parser_exists
    )

    formatter_init_data = init_data_model.InitDataModel(
        plugin_name=self.name,
        is_create_template=not self.init_formatter_exists
    )
    content_init_parser = parser_init_mapper.GetRenderedTemplate(
        parser_init_data)
    content_init_formatter = formatter_init_mapper.GetRenderedTemplate(
        formatter_init_data)
    content_parser = parser_mapper.GetRenderedTemplate(parser_data)
    content_formatter = formatter_mapper.GetRenderedTemplate(formatter_data)
    content_parser_test = parser_test_mapper.GetRenderedTemplate(
        parser_test_data)
    content_formatter_test = formatter_test_mapper.GetRenderedTemplate(
        formatter_test_data)

    formatter = file_handler.AddContent(
        self.path_helper.formatter_file_path, content_formatter)
    parser = file_handler.AddContent(
        self.path_helper.parser_file_path, content_parser)
    formatter_test = file_handler.AddContent(
        self.path_helper.formatter_test_file_path, content_formatter_test)
    parser_test = file_handler.AddContent(
        self.path_helper.parser_test_file_path, content_parser_test)
    database = file_handler.CopyFile(
        self.database, self.path_helper.database_path)
    parser_init = file_handler.AddContent(
        self.path_helper.parser_init_file_path, content_init_parser)
    formatter_init = file_handler.AddContent(
        self.path_helper.formatter_init_file_path, content_init_formatter)

    self._Print(formatter, parser, formatter_test, parser_test, database,
                parser_init, formatter_init)

  def _Print(
      self, formatter: str, parser: str, formatter_test: str,
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
    self._PrintCreate(formatter)
    self._PrintCreate(parser)
    self._PrintCreate(formatter_test)
    self._PrintCreate(parser_test)
    self._PrintCopy(database)
    if self.init_parser_exists:
      self._PrintEdit(parser_init)
    else:
      self._PrintCreate(parser_init)
    if self.init_formatter_exists:
      self._PrintEdit(formatter_init)
    else:
      self._PrintCreate(formatter_init)

  def _PrintCopy(self, file: str):
    """Print for copy file.

    Args:
      file (str): the file path
    """
    self.output.PrintInfo('copy ' + file)

  def _PrintEdit(self, file: str):
    """Print for edit file.

    Args:
      file (str): the file path
    """
    self.output.PrintInfo('edit ' + file)

  def _PrintCreate(self, file: str):
    """Print for create file.

    Args:
      file (str): the file path
    """
    self.output.PrintInfo('create ' + file)
