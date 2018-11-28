# -*- coding: utf-8 -*-
"""Turbinia job scaffolder."""
from l2tscaffolder.scaffolders import turbinia
from l2tscaffolder.scaffolders import manager


class TurbiniaJobTaskScaffolder(turbinia.TurbiniaBaseScaffolder):
  """The Turbinia job and task plugin scaffolder."""

  # The name of the plugin or parser this scaffolder provides.
  NAME = 'turbinia_job'
  DESCRIPTION = (
      'Provides a scaffolder to generate a Turbinia job plugin.')

  # Filenames of templates.
  TEMPLATE_JOB_FILE = 'turbinia_job.jinja2'
  TEMPLATE_TASK_FILE = 'turbinia_task.jinja2'


manager.ScaffolderManager.RegisterScaffolder(TurbiniaJobTaskScaffolder)
