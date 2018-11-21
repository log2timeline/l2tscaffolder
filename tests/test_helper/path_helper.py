# -*- coding: utf-8 -*-
"""helper for the test"""
import os

__file__ = os.path.abspath(__file__)


def TemplatePath() -> str:
  """ generating the template path for the tests

  Returns:
    str: the template path

  """
  return os.path.join(
      os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
      'l2tscaffolder', 'bll', 'templates')


def TestTemplatePath() -> str:
  """ generating the template path for the tests

  Returns:
    str: the template path

  """
  return os.path.join(
      os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
      'tests', 'test_template')


def TestDatabasePath() -> str:
  """ generating the template path for the tests

  Returns:
    str: the template path

  """
  return os.path.join(
      os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
      'tests', 'test_database')


def YapfStyleFilePath() -> str:
  """ gets the path to the yapf style file.

  Returns:
    str: the yapf file path
  """
  return os.path.join(
      os.path.dirname(os.path.dirname(__file__)),
      '.style.yapf')
