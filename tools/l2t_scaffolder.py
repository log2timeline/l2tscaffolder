# !/usr/bin/python
# -*- coding: utf-8 -*-
"""The l2t scaffolder tool."""
import click

from plasoscaffolder.frontend import cli_output_handler
from plasoscaffolder.frontend import frontend


@click.command()
@click.argument(
    'definition', envvar='SCAFFOLDER_DEFINITION', type=str, default='')
def StartCli(definition):
  """Generates templates for parser and plugins for l2t developers.

  This is a l2t scaffolder, used to generate templates for all plugin
  and parser creation for l2t tools.
  """
  output_handler = cli_output_handler.OutputHandlerClick()
  cli = frontend.ScaffolderFrontend(output_handler)

  cli.Start(definition)


if __name__ == '__main__':
  StartCli()  # pylint: disable=no-value-for-parameter
