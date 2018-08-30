# -*- coding: utf-8 -*-
"""Plaso scaffolder that generates plaso parser and plugins."""
import os

from typing import Iterator
from typing import List
from typing import Tuple
from typing import Type

from plasoscaffolder.lib import definitions
from plasoscaffolder.lib import mapping_helper
from plasoscaffolder.scaffolders import interface


class PlasoScaffolder(interface.Scaffolder):
  """The plaso scaffolder interface."""

  # The name of the plugin or parser this scaffolder plugin provides.
  NAME = 'plaso_base'

  # One liner describing what the scaffolder provides.
  DESCRIPTION = 'This is a scaffolder for plaso parsers and/or plugins'

  # Plugin type can be either 'parser' or 'plugin'.
  # If this is a plugin a plugin directory is based off the NAME attribute.
  PLUGIN_TYPE = 'parser'

  # Define which project this particular scaffolder belongs to.
  PROJECT = definitions.DEFINITION_PLASO

  # Filename of templates.
  TEMPLATE_PARSER_FILE = 'generic_plaso_parser.jinja2'
  TEMPLATE_PARSER_TEST = 'generic_plaso_parser_test.jinja2'
  TEMPLATE_FORMATTER_FILE = 'generic__plaso_formatter.jinja2'
  TEMPLATE_FORMATTER_TEST = 'generic_plaso_formatter_test.jinja2'

  # Questions, a list that contains all the needed questions that the
  # user should be prompted about before the plugin or parser is created.
  # Each element in the list should be of the named tuple question.
  QUESTIONS = []

  def __init__(self):
    """Initializes the plaso scaffolder."""
    super(PlasoScaffolder, self).__init__()
    self._formatter_path = ''
    self._formatter_test_path = ''
    self._parser_path = ''
    self._parser_test_path = ''
    self._mapping_helper = mapping_helper.ParserMapper()

  def _GenerateFormatter(self) -> str:
    """Generate the formatter file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_FORMATTER_FILE, self._attributes)

  def _GenerateFormatterTest(self) -> str:
    """Generate the formatter test file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_FORMATTER_TEST, self._attributes)

  def _GenerateParser(self) -> str:
    """Generate the parser file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_PARSER_FILE, self._attributes)

  def _GenerateParserTest(self) -> str:
    """Generate the parser test file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_PARSER_TEST, self._attributes)

  def GetQuestions(self) -> List[Type[interface.Scaffolder]]:
    """Return back a list of all questions."""
    questions = self.QUESTIONS
    questions.append(interface.Question(
        'test_file', 'Path to the test file.',
        'Path to a test file used by the parser or plugin.', str))
    return questions

  def GenerateFiles(self) -> Iterator[Tuple[str, str]]:
    """Generate all the files required for a plaso parser or a plugin.

    Yields:
      list: file name and content of the file to be written to disk.
    """
    parser_name = '{0:s}.py'.format(self._output_name)

    self._attributes['class_name'] = self._mapping_helper.GenerateClassName(
        self._output_name)

    if self.PLUGIN_TYPE == 'parser':
      self._attributes['parser_name'] = self._output_name
    else:
      self._attributes['plugin_name'] = self._output_name

    yield os.path.join(self._parser_path, parser_name), self._GenerateParser()

    yield os.path.join(
        self._parser_test_path, parser_name), self._GenerateParserTest()

    yield os.path.join(
        self._formatter_path, parser_name), self._GenerateFormatter()

    yield os.path.join(
        self._formatter_test_path, parser_name), self._GenerateFormatterTest()

    formatter_string = (
        '# TODO: put in alpha order.\nfrom plaso.formatters import'
        '{0:s}').format(self._output_name)
    yield os.path.join(self._formatter_path, '__init__.py'), formatter_string

    parser_string = (
        '# TODO: put in alpha order.\nfrom {0:s} import {1:s}').format(
            self._parser_path.replace(os.sep, '.'), self._output_name)
    yield os.path.join(self._parser_path, '__init__.py'), parser_string

  def GetFilesToCopy(self) -> Iterator[Tuple[str, str]]:
    """Return a list of files that need to be copied.

    Yields:
      tuple (str, str): file name of source and destination.
    """
    test_file = self._attributes.get('test_file', '')
    test_file_name = os.path.basename(test_file)
    test_file_path = os.path.join('test_data', test_file_name)

    self._attributes['test_file_path'] = test_file_path
    yield test_file, test_file_path

  def SetupScaffolder(self):
    """Sets up the scaffolder."""
    super(PlasoScaffolder, self).SetupScaffolder()
    self._parser_path = os.path.join('plaso', 'parsers')
    self._parser_test_path = os.path.join('tests', 'parsers')

    if self.PLUGIN_TYPE == 'plugin':
      plugin_path_name = '{0:s}_plugins'.format(self.NAME)
      self._parser_path = os.path.join(self._parser_path, plugin_path_name)
      self._parser_test_path = os.path.join(
          self._parser_test_path, plugin_path_name)

    self._formatter_path = os.path.join('plaso', 'formatters')
    self._formatter_test_path = os.path.join('tests', 'formatters')

    self._mapping_helper.SetDefaultPaths()
