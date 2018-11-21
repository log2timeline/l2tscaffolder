# -*- coding: utf-8 -*-
"""Timesketch sketch analyzer scaffolder."""

from l2tscaffolder.scaffolders import timesketch
from l2tscaffolder.scaffolders import manager


class TimesketchSketchScaffolder(timesketch.TimesketchBaseScaffolder):
  """The Timesketch sketch analyzer plugin scaffolder."""

  # The name of the plugin or parser this scaffolder provides.
  NAME = 'sketch_analyzer'
  DESCRIPTION = (
      'Provides a scaffolder to generate a Timesketch sketch analyzer plugin.')

  # Filenames of templates.
  TEMPLATE_PLUGIN_FILE = 'ts_sketch_analyzer.jinja2'
  TEMPLATE_PLUGIN_TEST = 'ts_sketch_analyzer_test.jinja2'


manager.ScaffolderManager.RegisterScaffolder(TimesketchSketchScaffolder)
