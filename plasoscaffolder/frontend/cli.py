# !/usr/bin/python
# -*- coding: utf-8 -*-
"""The scaffolder CLI frontend."""

import click

from plasoscaffolder.frontend import cli_output_handler
from plasoscaffolder.frontend import frontend


class ScaffolderCli(frontend.ScaffolderFrontend):
  """A CLI implementation for the scaffolder project.

  Attributes:
    OUTPUT_HANDLER (cli_output_handler.OutputHandlerClick: output handler
        that is used to request and read input from end user.
  """

  OUTPUT_HANDLER = cli_output_handler.OutputHandlerClick()

  @classmethod
  def Start(
      cls, unused_ctx: click.core.Context, unused_param: click.core.Option,
      value: str):
    """Start the CLI.

    Args:
      unused_ctx (click.core.Context): the click context (automatically given
        via callback)
      unused_param (click.core.Option): the click command (automatically
        given via callback)
      value (str): the definition string (automatically given via callback)
    """
    super(ScaffolderCli, cls).Start(value)
