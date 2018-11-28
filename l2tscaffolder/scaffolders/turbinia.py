# -*- coding: utf-8 -*-
"""Turbinia component scaffolder."""
import datetime
import os
import logging

from typing import Dict
from typing import Iterator
from typing import Tuple

from l2tscaffolder.lib import definitions
from l2tscaffolder.lib import mapping_helper
from l2tscaffolder.scaffolders import interface


class TurbiniaBaseScaffolder(interface.Scaffolder):
  """The Turbinia base scaffolder interface.

  Attributes:
    class_name (str): class name of the Turbinia plugin to be generated.
  """

  # The name of the plugin this scaffolder plugin provides.
  NAME = 'turbinia_base'

  # One liner describing what the scaffolder provides.
  DESCRIPTION = 'This is a scaffolder for Turbinia components'

  # Define which project this particular scaffolder belongs to.
  PROJECT = definitions.DEFINITION_TURBINIA

  # Filename of templates.
  TEMPLATE_JOB_FILE = None
  TEMPLATE_TASK_FILE = None

  def __init__(self):
    """Initializes the Turbinia scaffolder."""
    super(TurbiniaBaseScaffolder, self).__init__()
    self._plugin_path = os.path.join('turbinia', 'jobs')
    self._task_path = os.path.join('turbinia', 'workers')
    self._mapping_helper = mapping_helper.MappingHelper()

    self.class_name = ''

  def _GenerateJobFile(self) -> str:
    """Generates the job plugin file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_JOB_FILE, self.GetJinjaContext())

  def _GenerateTaskFile(self) -> str:
    """Generates the task plugin file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_TASK_FILE, self.GetJinjaContext())

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
    context = super(TurbiniaBaseScaffolder, self).GetJinjaContext()
    context['class_name'] = self.class_name
    context['plugin_name'] = self._output_name
    time_now = datetime.datetime.utcnow()
    context['year'] = time_now.year

    return context

  def GenerateFiles(self) -> Iterator[Tuple[str, str]]:
    """Generates all the files required for a Turbinia component.

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
      plugin_content = self._GenerateJobFile()
      yield plugin_path, plugin_content
    except SyntaxError as exception:
      logging.error((
          'Syntax error while attempting to generate component, error '
          'message: {0!s}').format(exception))

    try:
      task_path = os.path.join(self._task_path, plugin_name)
      task_content = self._GenerateTaskFile()
      yield task_path, task_content
    except SyntaxError as exception:
      logging.error((
          'Syntax error while attempting to generate component, error '
          'message: {0!s}').format(exception))
