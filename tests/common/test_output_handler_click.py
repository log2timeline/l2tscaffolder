# -*- coding: utf-8 -*-
# disable pylint unused-argument because it is used for the mock
# pylint: disable=unused-argument
# disable pylint bare-except because it should fail at any exception
# pylint: disable=bare-except
# pylint: disable=redundant-unittest-assert
"""test class"""
import unittest
from unittest.mock import patch

from click import testing
from plasoscaffolder.common import output_handler_click


class ClickOutputHandler(unittest.TestCase):
  """testing the file output handler"""

  def setUp(self):
    self.click = output_handler_click.OutputHandlerClick()

  @patch('click.prompt', return_value='yes')
  def testPromptInfo(self, prompt):
    """test prompt info"""
    result = self.click.PromptInfo('test')
    self.assertEqual('yes', result)

  @patch('click.prompt', return_value='yes')
  def testPromptError(self, prompt):
    """test prompt info"""
    result = self.click.PromptError('test')
    self.assertEqual('yes', result)

  @patch('click.prompt', return_value='yes')
  def testPromptInfoWithDefault(self, prompt):
    """test prompt info"""
    result = self.click.PromptInfoWithDefault('text', int, 1)
    self.assertEqual('yes', result)

  def testPrintInfo(self):
    """test print info."""
    try:
      runner = testing.CliRunner()
      runner.invoke(self.click.PrintInfo('info'))
    except:
      self.assertTrue(False)

  def testPrintError(self):
    """test print error."""
    try:
      runner = testing.CliRunner()
      runner.invoke(self.click.PrintError('info'))
    except:
      self.assertTrue(False)

  @patch('click.confirm', return_value='True')
  def testConfirmIfTrue(self, confirm):
    """test Confirm if confirmed"""
    result = self.click.Confirm(default=True, abort=False, text='text')
    self.assertEqual('True', result)

  @patch('click.confirm', return_value='False')
  def testConfirmIfFalse(self, confirm):
    """test Confirm if not confirmed"""
    result = self.click.Confirm(default=False, abort=False, text='text')
    self.assertEqual('False', result)
