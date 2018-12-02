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
from l2tscaffolder.scaffolders import manager


class TurbiniaJobTaskScaffolder(interface.Scaffolder):
  """The Turbinia base scaffolder interface.

  Attributes:
    class_name (str): class name of the Turbinia job and task to be generated.
  """

  # The name of the scaffolder plugin.
  NAME = 'turbinia_job_and_task'

  # One liner describing what the scaffolder provides.
  DESCRIPTION = (
      'Provides a scaffolder to generate a Turbinia job and task plugins.')

  # Define which project this particular scaffolder belongs to.
  PROJECT = definitions.DEFINITION_TURBINIA

  # Filenames of templates.
  TEMPLATE_JOB_FILE = 'turbinia_job.jinja2'
  TEMPLATE_TASK_FILE = 'turbinia_task.jinja2'

  def __init__(self):
    """Initializes the Turbinia scaffolder."""
    super(TurbiniaJobTaskScaffolder, self).__init__()
    self._job_path = os.path.join('turbinia', 'jobs')
    self._task_path = os.path.join('turbinia', 'workers')
    self._mapping_helper = mapping_helper.MappingHelper()

    self.class_name = ''

  def _GenerateJobFile(self) -> str:
    """Generates the job job file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_JOB_FILE, self.GetJinjaContext())

  def _GenerateTaskFile(self) -> str:
    """Generates the task file."""
    return self._mapping_helper.RenderTemplate(
        self.TEMPLATE_TASK_FILE, self.GetJinjaContext())

  def GetInitFileChanges(self) -> Iterator[Tuple[str, str]]:
    """Generate a list of init files that need changing and the changes to them.

    Yields:
      Tuple[str, str]: path to the init file and the entry to add to it.
    """
    python_init_path = self._job_path.replace(os.sep, '.')
    job_string = 'from {0:s} import {1:s}\n'.format(
        python_init_path, self._output_name)
    job_init_path = os.path.join(self._job_path, '__init__.py')
    yield job_init_path, job_string

  def GetJinjaContext(self) -> Dict[str, object]:
    """Returns a dict that can be used as a context for Jinja2 templates.

    Returns:
      dict: containing:
        str: name of Jinja argument.
        object: Jinja argument value.
    """
    context = super(TurbiniaJobTaskScaffolder, self).GetJinjaContext()
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
      job_path = os.path.join(self._job_path, plugin_name)
      job_content = self._GenerateJobFile()
      yield job_path, job_content
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


manager.ScaffolderManager.RegisterScaffolder(TurbiniaJobTaskScaffolder)
