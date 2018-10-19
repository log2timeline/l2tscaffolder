# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test class for the CLI frontend."""
import unittest

from plasoscaffolder.frontend import cli


class FrontendCLITest(unittest.TestCase):
  """Test case for the frontend CLI. """

  @classmethod
  def setUpClass(cls):
    """Sets up the test class."""
    # Need to make sure there are no registered projects, and can't iterate
    # directly over projects since changing the dict in the middle of an iter
    # causes errors.
    pass

  def testGetDefinitionNames(self):
    """Test getting definition names."""
    pass


if __name__ == '__main__':
  unittest.main()

"""
  def CreateGitFeatureBranch(cls, project_path: str, module_name: str):
  def GatherScaffolderAnswers(cls, scaffolder, scaffolder_engine):
  def GetDefinition(
  def GetModuleName(cls) -> str:
  def GetProjectPath(
  def GetScaffolder(
"""
