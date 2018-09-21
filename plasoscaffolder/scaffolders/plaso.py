# -*- coding: utf-8 -*-
"""Plaso scaffolder that generates plaso parser and plugins."""
import os
import logging

from typing import Dict
from typing import Iterator
from typing import List
from typing import Tuple
from typing import Type

from plasoscaffolder.lib import definitions
from plasoscaffolder.lib import errors
from plasoscaffolder.lib import mapping_helper
from plasoscaffolder.scaffolders import interface


class PlasoBaseScaffolder(interface.Scaffolder):
  """The plaso base scaffolder interface."""

  # The name of the plugin or parser this scaffolder plugin provides.
  NAME = 'plaso_base'

  # One liner describing what the scaffolder provides.
  DESCRIPTION = 'This is a scaffolder for plaso parsers and/or plugins'

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
    super(PlasoBaseScaffolder, self).__init__()
    self._formatter_path = os.path.join('plaso', 'formatters')
    self._formatter_test_path = os.path.join('tests', 'formatters')
    self._parser_path = os.path.join('plaso', 'parsers')
    self._parser_test_path = os.path.join('tests', 'parsers')
    self._mapping_helper = mapping_helper.ParserMapper()
    self._mapping_helper.SetDefaultPaths()

    self.class_name = ''
    self.test_file = ''
    self.test_file_path = ''

  def _GenerateFormatter(self) -> str:
    """Generates the formatter file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_FORMATTER_FILE, self.GetJinjaContext())

  def _GenerateFormatterTest(self) -> str:
    """Generates the formatter test file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_FORMATTER_TEST, self.GetJinjaContext())

  def _GenerateParser(self) -> str:
    """Generates the parser file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_PARSER_FILE, self.GetJinjaContext())

  def _GenerateParserTest(self) -> str:
    """Generates the parser test file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_PARSER_TEST, self.GetJinjaContext())

  def GetJinjaContext(self) -> Dict[str, object]:
    """Returns a dict that can be used as a context for Jinja2 templates."""
    context = super(PlasoBaseScaffolder, self).GetJinjaContext()

    context['class_name'] = self.class_name
    context['test_file'] = self.test_file
    context['test_file_path'] = self.test_file_path

    return context

  def GetQuestions(self) -> List[Type[interface.Scaffolder]]:
    """Returns scaffolder questions as well as adding plaso related ones."""
    questions = self.QUESTIONS
    questions.append(interface.Question(
        'test_file',
        'Absolute or relative path to the file that will be used for tests.',
        'Path to a test file used by the parser or plugin.', str))
    return questions

  def GenerateFiles(self) -> Iterator[Tuple[str, str]]:
    """Generates all the files required for a plaso parser or a plugin.

    Yields:
      list: file name and content of the file to be written to disk.
    """
    parser_name = '{0:s}.py'.format(self._output_name)

    self.class_name = self._mapping_helper.GenerateClassName(
        self._output_name)

    try:
      parser_path = os.path.join(self._parser_path, parser_name)
      parser_content = self._GenerateParser()
      yield parser_path, parser_content
    except SyntaxError as exception:
      logging.error((
          'Syntax error while attempting to generate parser, error '
          'message: {0!s}').format(exception))

    try:
      test_path = os.path.join(self._parser_test_path, parser_name)
      test_content = self._GenerateParserTest()
      yield test_path, test_content
    except SyntaxError as exception:
      logging.error((
          'Syntax error while attempting to generate parser test, error '
          'message: {0!s}').format(exception))

    try:
      formatter_path = os.path.join(self._formatter_path, parser_name)
      formatter_content = self._GenerateFormatter()
      yield formatter_path, formatter_content
    except SyntaxError as exception:
      logging.error((
          'Syntax error while attempting to generate formatter, error '
          'message: {0!s}').format(exception))

    try:
      formatter_test_path = os.path.join(self._formatter_test_path, parser_name)
      formatter_test_content = self._GenerateFormatterTest()
      yield formatter_test_path, formatter_test_content
    except SyntaxError as exception:
      logging.error((
          'Syntax error while attempting to generate formatter test, error '
          'message: {0!s}').format(exception))

    formatter_string = (
        '# TODO: put in alphabetical order.\nfrom plaso.formatters import'
        '{0:s}').format(self._output_name)
    formatter_init_path = os.path.join(self._formatter_path, '__init__.py')
    yield formatter_init_path, formatter_string

    parser_string = (
        '# TODO: put in alphabetical order.\nfrom {0:s} import {1:s}').format(
            self._parser_path.replace(os.sep, '.'), self._output_name)
    parser_init_path = os.path.join(self._parser_path, '__init__.py')
    yield parser_init_path, parser_string

  def GetFilesToCopy(self) -> Iterator[Tuple[str, str]]:
    """Return a list of files that need to be copied.

    Raises:
      IOError: when the test file does not exist.

    Yields:
      tuple (str, str): file name of source and destination.
    """
    if not self.test_file:
      raise IOError('A plaso parser cannot be generated without a test file.')

    if not os.path.isfile(self.test_file):
      raise IOError('Test file [{0:s}] does not exist.'.format(self.test_file))

    test_file_name = os.path.basename(self.test_file)
    self.test_file_path = os.path.join('test_data', test_file_name)

    yield test_file_name, self.test_file_path

  def RaiseIfNotReady(self):
    """Checks to see if all attributes are set to start generating files.

    Raises:
      ScaffolderNotConfigured: if the scaffolder is not fully configured.
    """
    super(PlasoBaseScaffolder, self).RaiseIfNotReady()
    if not os.path.isfile(self.test_file):
      errors.ScaffolderNotConfigured(
          'Test file path is incorrect, file does not exist.')


class PlasoPluginScaffolder(PlasoBaseScaffolder):
  """Scaffolder for generating plaso plugins."""

  def __init__(self):
    """Initializes the plaso plugin scaffolder."""
    super(PlasoPluginScaffolder, self).__init__()
    plugin_path_name = '{0:s}_plugins'.format(self.NAME)
    self._parser_path = os.path.join(self._parser_path, plugin_path_name)
    self._parser_test_path = os.path.join(
        self._parser_test_path, plugin_path_name)

    self.plugin_name = ''

  def GetJinjaContext(self) -> Dict[str, object]:
    """Returns a dict that can be used as a context for Jinja2 templates."""
    context = super(PlasoPluginScaffolder, self).GetJinjaContext()
    context['plugin_name'] = self._output_name
    return context


class PlasoParserScaffolder(PlasoBaseScaffolder):
  """Scaffolder for generating plaso parsers."""

  def __init__(self):
    """Initializes the plaso plugin scaffolder."""
    super(PlasoParserScaffolder, self).__init__()
    self.parser_name = ''

  def GetJinjaContext(self) -> Dict[str, object]:
    """Returns a dict that can be used as a context for Jinja2 templates."""
    context = super(PlasoBaseScaffolder, self).GetJinjaContext()
    context['parser_name'] = self._output_name
    return context
