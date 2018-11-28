# -*- coding: utf-8 -*-
"""Plaso scaffolder that generates plaso parser and plugins."""
import os
import logging

from typing import Dict
from typing import Iterator
from typing import List
from typing import Tuple

from l2tscaffolder.lib import definitions
from l2tscaffolder.lib import errors
from l2tscaffolder.lib import mapping_helper
from l2tscaffolder.scaffolders import interface


class TestFileQuestion(interface.StringQuestion):
  """Test file question."""

  def ValidateAnswer(self, answer: str):
    """Validates the answer to the test file question.

    Args:
      answer (str): path to a test file.

    Raises:
      errors.UnableToConfigure: if the answer is invalid.
    """
    super(TestFileQuestion, self).ValidateAnswer(answer)

    if not os.path.isfile(answer):
      raise errors.UnableToConfigure(
          'The test file {0:s} does not exist.'.format(answer))


class PlasoBaseScaffolder(interface.Scaffolder):
  """The plaso base scaffolder interface.

  Attributes:
    class_name (str): class name of the plaso parser or plugin to be generated.
    test_file (str): name of the file used for testing the parser or plugin.
    test_file_path (str): path to the test file.
  """

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
    self._mapping_helper = mapping_helper.MappingHelper()

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

  def GetInitFileChanges(self) -> Iterator[Tuple[str, str]]:
    """Generate a list of init files that need changing and the changes to them.

    Yields:
      Tuple[str, str]: path to the init file and the entry to add to it.
    """
    formatter_string = 'from plaso.formatters import {0:s}\n'.format(
        self._output_name)
    formatter_init_path = os.path.join(self._formatter_path, '__init__.py')
    yield formatter_init_path, formatter_string

    parser_string = 'from {0:s} import {1:s}\n'.format(
        self._parser_path.replace(os.sep, '.'), self._output_name)
    parser_init_path = os.path.join(self._parser_path, '__init__.py')
    yield parser_init_path, parser_string

  def GetJinjaContext(self) -> Dict[str, object]:
    """Returns a dict that can be used as a context for Jinja2 templates.

    Returns:
      dict: containing:
        str: name of Jinja argument.
        object: Jinja argument value.
    """
    context = super(PlasoBaseScaffolder, self).GetJinjaContext()

    context['class_name'] = self.class_name
    context['test_file'] = self.test_file
    context['test_file_path'] = self.test_file_path

    return context

  def GetQuestions(self) -> List[interface.BaseQuestion]:
    """Returns scaffolder questions as well as adding plaso related ones.

    Returns:
      list[interface.BaseQuestion]: questions to prompt the user with.
    """
    test_file_question = TestFileQuestion(
        'test_file',
        'Absolute or relative path to the file that will be used for tests.')
    questions = self.QUESTIONS
    questions.append(test_file_question)
    return questions

  def GenerateFiles(self) -> Iterator[Tuple[str, str]]:
    """Generates all the files required for a plaso parser or a plugin.

    Yields:
      list[tuple]: containing:
       str: file name.
       str: file content.
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

    test_path = os.path.join(self._parser_test_path, parser_name)
    try:
      test_content = self._GenerateParserTest()
      yield test_path, test_content
    except SyntaxError as exception:
      logging.error((
          'Syntax error while attempting to generate parser test, error '
          'message: {0!s}').format(exception))

    formatter_path = os.path.join(self._formatter_path, parser_name)
    try:
      formatter_content = self._GenerateFormatter()
      yield formatter_path, formatter_content
    except SyntaxError as exception:
      logging.error((
          'Syntax error while attempting to generate formatter, error '
          'message: {0!s}').format(exception))

    formatter_test_path = os.path.join(self._formatter_test_path, parser_name)
    try:
      formatter_test_content = self._GenerateFormatterTest()
      yield formatter_test_path, formatter_test_content
    except SyntaxError as exception:
      logging.error((
          'Syntax error while attempting to generate formatter test, error '
          'message: {0!s}').format(exception))

  # pylint raises issues with OSError being raised and not documented, but it is
  # not raised.
  # pylint: disable=missing-raises-doc
  def GetFilesToCopy(self) -> Iterator[Tuple[str, str]]:
    """Return a list of files that need to be copied.

    Raises:
      IOError: when the test file does not exist.

    Yields:
      tuple: containing:
        str: file name of source.
        str: file name of destination.
    """
    if not self.test_file:
      raise IOError('A plaso parser cannot be generated without a test file.')

    if not os.path.isfile(self.test_file):
      raise IOError('Test file [{0:s}] does not exist.'.format(self.test_file))

    test_file_name = os.path.basename(self.test_file)
    self.test_file_path = os.path.join('test_data', test_file_name)

    yield self.test_file, self.test_file_path

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
    """Returns a dict that can be used as a context for Jinja2 templates.

    Returns:
      dict: containing:
        str: name of Jinja argument.
        object: Jinja argument value.
    """
    context = super(PlasoPluginScaffolder, self).GetJinjaContext()
    context['plugin_name'] = self._output_name
    return context


class PlasoParserScaffolder(PlasoBaseScaffolder):
  """Scaffolder for generating plaso parsers.

  Attributes:
    parser_name(str): name of the parser to be generated.
  """

  def __init__(self):
    """Initializes the plaso plugin scaffolder."""
    super(PlasoParserScaffolder, self).__init__()
    self.parser_name = ''

  def GetJinjaContext(self) -> Dict[str, object]:
    """Returns a dict that can be used as a context for Jinja2 templates.

    Returns:
      dict: containing:
        str: name of Jinja argument.
        object: Jinja argument value.
    """
    context = super(PlasoParserScaffolder, self).GetJinjaContext()
    context['parser_name'] = self._output_name
    return context
