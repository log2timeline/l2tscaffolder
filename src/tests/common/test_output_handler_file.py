# -*- coding: utf-8 -*-
"""test class"""
import unittest

from tests.fake import fake_file_handler
from tests.test_helper import output_handler_file


class FileOutputHandler(unittest.TestCase):
  """testing the file output handler"""

  def setUp(self):
    self.file_path = "testpath"
    self.output = output_handler_file.OutputHandlerFile(
        self.file_path,
        fake_file_handler.FakeFileHandler())

  def testPromptInfo(self):
    """test prompt info"""
    actual_file = self.output.PrintInfo("the mighty")
    self.assertEqual(self.file_path, actual_file)

  def test_prompt_error(self):
    """test prompt error"""
    actual_file = self.output.PrintInfo("the mighty")
    self.assertEqual(self.file_path, actual_file)

  def testPrintInfo(self):
    """test print info. should return the edited file"""
    actual_file = self.output.PrintInfo("the mighty")
    self.assertEqual(self.file_path, actual_file)

  def testPrintError(self):
    """test print error. should return the edited file"""
    actual_file = self.output.PrintError("the mighty")
    self.assertEqual(self.file_path, actual_file)

  def testConfirmIfTrue(self):
    """test Confirm if confirmed"""
    actual = self.output.Confirm("some message")
    self.assertTrue(actual)

  def testConfirmIfFalse(self):
    """test Confirm if not confirmed"""
    output = output_handler_file.OutputHandlerFile(
        None, None,
        confirm=False)

    with self.assertRaises(SystemExit):
      output.Confirm("")
