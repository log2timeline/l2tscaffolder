# -*- coding: utf-8 -*-
"""Timesketch index analyzer scaffolder."""
from plasoscaffolder.scaffolders import timesketch
from plasoscaffolder.scaffolders import manager


class TimesketchIndexScaffolder(timesketch.TimesketchBaseScaffolder):
  """The Timesketch index analyzer plugin scaffolder."""

  # The name of the plugin or parser this scaffolder provides.
  NAME = 'index_analyzer'
  DESCRIPTION = (
      'Provides a scaffolder to generate a Timesketch index analyzer plugin.')

  # Filenames of templates.
  TEMPLATE_PLUGIN_FILE = 'ts_index_analyzer.jinja2'
  TEMPLATE_PLUGIN_TEST = 'ts_index_analyzer_test.jinja2'


manager.ScaffolderManager.RegisterScaffolder(TimesketchIndexScaffolder)
