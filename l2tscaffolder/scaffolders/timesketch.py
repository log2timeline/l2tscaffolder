# -*- coding: utf-8 -*-
"""Timesketch scaffolder that generates analyzer plugins."""
import os
import logging

from typing import Dict
from typing import Iterator
from typing import Tuple

from l2tscaffolder.lib import definitions
from l2tscaffolder.lib import mapping_helper
from l2tscaffolder.scaffolders import interface


class TimesketchBaseScaffolder(interface.Scaffolder):
  """The Timesketch base scaffolder interface.

  Attributes:
    class_name (str): class name of the Timesketch analyzer to be generated.
  """

  # The name of the plugin this scaffolder plugin provides.
  NAME = 'timesketch_base'

  # One liner describing what the scaffolder provides.
  DESCRIPTION = 'This is a scaffolder for Timesketch analyzers'

  # Define which project this particular scaffolder belongs to.
  PROJECT = definitions.DEFINITION_TIMESKETCH

  # Filename of templates.
  TEMPLATE_PLUGIN_FILE = ''
  TEMPLATE_PLUGIN_TEST = ''

  # Questions, a list that contains all the needed questions that the
  # user should be prompted about before the plugin or parser is created.
  # Each element in the list should be of the named tuple question.
  QUESTIONS = []

  def __init__(self):
    """Initializes the Timesketch scaffolder."""
    super(TimesketchBaseScaffolder, self).__init__()
    self._plugin_path = os.path.join('timesketch', 'lib', 'analyzers')
    self._plugin_test_path = os.path.join('timesketch', 'lib', 'analyzers')
    # Timesketch uses 4 spaces instead of 2, thus we need to set a different
    # formatter.
    self._mapping_helper = mapping_helper.MappingHelper(
        formatter_path='.style.ts.yapf')

    self.class_name = ''

  def _GeneratePlugin(self) -> str:
    """Generates the plugin file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_PLUGIN_FILE, self.GetJinjaContext())

  def _GeneratePluginTest(self) -> str:
    """Generates the plugin test file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_PLUGIN_TEST, self.GetJinjaContext())

  def GetInitFileChanges(self) -> Iterator[Tuple[str, str]]:
    """Generate a list of init files that need changing and the changes to them.

    Yields:
      Tuple[str, str]: path to the init file and the entry to add to it.
    """
    plugin_path = self._plugin_path.replace(os.sep, '.')
    plugin_string = 'from {0:s} import {1:s}\n'.format(
        plugin_path, self._output_name)
    plugin_init_path = os.path.join(self._plugin_path, '__init__.py')
    yield plugin_init_path, plugin_string

  def GetFilesToCopy(self) -> Iterator[Tuple[str, str]]:
    """Return a list of files that need to be copied.

    Returns:
      an empty iterator.
    """
    return iter(())

  def GetJinjaContext(self) -> Dict[str, object]:
    """Returns a dict that can be used as a context for Jinja2 templates.

    Returns:
      dict: containing:
        str: name of Jinja argument.
        object: Jinja argument value.
    """
    context = super(TimesketchBaseScaffolder, self).GetJinjaContext()
    context['class_name'] = self.class_name
    context['plugin_name'] = self._output_name

    return context

  def GenerateFiles(self) -> Iterator[Tuple[str, str]]:
    """Generates all the files required for a Timesketch analyzer plugin.

    Yields:
      list[tuple]: containing:
       str: file name.
       str: file content.
    """
    plugin_name = '{0:s}.py'.format(self._output_name)

    self.class_name = self._mapping_helper.GenerateClassName(
        self._output_name)

    try:
      plugin_path = os.path.join(self._plugin_path, plugin_name)
      plugin_content = self._GeneratePlugin()
      yield plugin_path, plugin_content
    except SyntaxError as exception:
      logging.error((
          'Syntax error while attempting to generate plugin, error '
          'message: {0!s}').format(exception))

    test_file_name = '{0:s}_test.py'.format(self._output_name)
    test_path = os.path.join(self._plugin_test_path, test_file_name)
    try:
      test_content = self._GeneratePluginTest()
      yield test_path, test_content
    except SyntaxError as exception:
      logging.error((
          'Syntax error while attempting to generate plugin test, error '
          'message: {0!s}').format(exception))
