# !/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# Docstrings are used by click in generating output. Since we don't want this
#  behavior the following functions do not contain docstrings.

"""The start point of the plasoscaffolder."""
import click

from plasoscaffolder.frontend.sqliteplugin import commands as sqliteplugin


@click.group()
def entry_point():
  pass


# handles the click initialization
entry_point.add_command(sqliteplugin.sqlite)

if __name__ == '__main__':
  entry_point()
