# !/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: disable=unused-argument
# pylint: disable=no-value-for-parameter
# Docstrings are used by click in generating output. Since we don't want this
#  behavior the following functions do not contain docstrings.

"""The l2t scaffolder tool."""
import click

from plasoscaffolder.frontend import cli


@click.command()
@click.option(
    '--definition', envvar='SCAFFOLDER_DEFINITION', default='',
    help='Project or definition to choose.', callback=cli.ScaffolderCli.Start)
def StartCli(definition):
  pass


if __name__ == '__main__':
  StartCli()
