# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test class for the CLI frontend."""
import io
import os
import re
import unittest
from unittest.mock import MagicMock
import tempfile

from l2tscaffolder.definitions import manager as definition_manager
from l2tscaffolder.definitions import plaso
from l2tscaffolder.frontend import frontend
from l2tscaffolder.frontend import output_handler
from l2tscaffolder.scaffolders import manager as scaffolder_manager
from l2tscaffolder.scaffolders import plaso_sqlite


class TestOutputHandler(output_handler.BaseOutputHandler):
  """Test implementation of the output handler."""

  def __init__(self):
    """Initializes the test output handler."""
    self._data = []
    self._output = None

  def _GetInput(self):
    """Returns a line from the data, or an empty string if no data."""
    if not self._data:
      return ''

    return self._data.pop(0)

  def Confirm(self, text: str, default=True, abort=True):
    """Ask for a confirmation, either yes or no to a question.

    Args:
      text (str): prompts the user for a confirmation, with the given test as
          the question
      default (bool): the default for the confirmation answer. If True the
          default is Y(es), if False the default is N(o)
      abort (bool): if the program should abort if the user answer to the
          confirm prompt is no. The default is an abort.

    Returns:
       bool: False if the user entered no, True if the user entered yes
    """
    answer = self._GetInput()
    if answer.lower() in ['n', 'no']:
      return False

    return True

  def FeedLine(self, line):
    """Feed the handler with a line."""
    self._data.append(line)

  def PrintError(self, text: str):
    """A echo for errors with click.

    Args:
      text (str): the text to print
    """
    self._output.write(text)

  def PrintInfo(self, text: str):
    """A echo for information with click.

    Args:
      text (str): the text to print
    """
    self._output.write(text)

  def PrintNewLine(self):
    """A new line added to output."""
    self._output.write('\n')

  def PrintOutput(self, text: str):
    """A echo for information with click.

    Args:
      text (str): the text to print.
    """
    self._output.write(text)

  def PromptError(self, text: str) -> str:
    """A prompt for errors with click.

    Args:
      text (str): the text to prompt

    Returns:
      str: the user input
    """
    self._output.write(text)
    return self._GetInput()

  def PromptInfo(self, text: str) -> str:
    """A prompt for information with click.

    Args:
      text (str): the text to  prompt

    Returns:
      str: the user input
    """
    self._output.write(text)
    return self._GetInput()

  def PromptInfoWithDefault(
      self, text: str, input_type: object, default: object) -> str:
    """A prompt for information, with a default value and a required type.

    Args:
      text (str): the text to prompt
      input_type (object): the type of the input
      default (object): the default value

    Returns:
      str: the user input
    """
    self._output.write('{0:s} [{1:s}]'.format(text, input_type))
    return self._GetInput()

  def SetOutput(self, output_writer):
    """Set the output writer."""
    self._output = output_writer


class TestFrontend(frontend.ScaffolderFrontend):
  """Test implementation of the frontend."""

  def __init__(self, output_handler_to_use):
    """Initializes the frontend."""
    super(TestFrontend, self).__init__(output_handler_to_use)
    self._mock = MagicMock()
    self._git_helper = self._mock

  def CreateGitFeatureBranch(self, project_path: str, module_name: str):
    """Mock creating feature branch."""
    branch_name = re.sub('(?<!^)(?=[A-Z])', '_', module_name).lower()
    self._output_handler.PrintOutput(
        'Created the feature branch: {0:s} inside {1:s}'.format(
            branch_name, project_path))

  def GetProjectPath(self, definition):
    """Returns the path to the project's root folder as chosen by the user.

    Args:
      definition (definition_interface.ScaffolderDefinition): the chosen
          definition. Used to validate the project path.

    Returns:
      str: the path to the project's root folder.

    Raises:
      errors.WrongCliInput: when no valid project path has been provided.
    """
    return_value = super(TestFrontend, self).GetProjectPath(definition)
    self._git_helper = self._mock
    return return_value


class ScaffolderFrontendTest(unittest.TestCase):
  """Test case for the scaffolder frontend."""

  # Temporary directory for mocking a plaso source tree.
  root_directory = None

  @classmethod
  def setUpClass(cls):
    """Set up the test class."""
    try:
      definition_manager.DefinitionManager.RegisterDefinition(
          plaso.PlasoProject)
    except KeyError:
      pass

    try:
      scaffolder_manager.ScaffolderManager.RegisterScaffolder(
          plaso_sqlite.PlasoSQLiteScaffolder)
    except KeyError:
      pass
    cls.root_directory = tempfile.TemporaryDirectory()
    root_dir_name = cls.root_directory.name
    os.mkdir(os.path.join(root_dir_name, 'plaso'))
    os.mkdir(os.path.join(root_dir_name, 'plaso', 'parsers'))
    os.mkdir(os.path.join(root_dir_name, 'plaso', 'test_data'))
    os.mkdir(os.path.join(root_dir_name, 'plaso', 'tests'))
    os.mkdir(os.path.join(root_dir_name, 'plaso', 'parsers', 'sqlite_plugins'))
    fw = open(os.path.join(root_dir_name, 'plaso.ini'), 'w')
    fw.write('\n')
    fw.close()

  @classmethod
  def tearDownClass(cls):
    """Cleans up after running tests."""
    cls.root_directory.cleanup()

  def testFrontend(self):
    """Tests the frontend.

    This test runs the entire front-end and tests to see if
    files are generated as expected.
    """
    string_buffer = io.StringIO()
    test_output_handler = TestOutputHandler()
    test_output_handler.SetOutput(string_buffer)

    test_output_handler.FeedLine(self.root_directory.name)
    test_output_handler.FeedLine('foobar test')
    test_output_handler.FeedLine('0')
    test_output_handler.FeedLine('FooQuery')
    test_output_handler.FeedLine('SELECT foo FROM bar;')
    test_output_handler.FeedLine('n')
    test_output_handler.FeedLine('bar')
    test_output_handler.FeedLine('n')
    cwd = os.getcwd()
    test_output_handler.FeedLine(
        os.path.join(cwd, 'test_data', 'test_sqlite.db'))
    test_output_handler.FeedLine('Y')

    test_frontend = TestFrontend(test_output_handler)
    test_frontend.Start('plaso')

    string_buffer.seek(0)
    lines = string_buffer.read().split('\n')
    first_line = lines[0]

    expected_string = (
        '== Starting the scaffolder ==Gathering required information.')
    self.assertEqual(first_line.strip(), expected_string)

    expected_string = 'written to disk.'
    last_line = lines[-1]
    last_part = last_line[-len(expected_string):]
    self.assertEqual(last_part, expected_string)

    self.assertTrue(os.path.isfile(os.path.join(
        self.root_directory.name, 'plaso', 'parsers', 'sqlite_plugins',
        'foobar_test.py')))
    self.assertTrue(os.path.isfile(os.path.join(
        self.root_directory.name, 'tests', 'parsers', 'sqlite_plugins',
        'foobar_test.py')))

    self.assertTrue(os.path.isfile(os.path.join(
        self.root_directory.name, 'test_data', 'test_sqlite.db')))


if __name__ == '__main__':
  unittest.main()
