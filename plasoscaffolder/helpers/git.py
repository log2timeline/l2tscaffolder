# -*- coding: utf-8 -*-
"""Git helper for the scaffolder project.

This file provides a class to assist with git operations.
"""
import os
import re

from typing import Tuple

from plasoscaffolder.helpers import cli
from plasoscaffolder.lib import errors

class GitHelper(cli.CLIHelper):
  """Helper class for git operations.

  Attributes:
    project_path: path to the git project folder.
  """

  def __init__(self, project_path: str):
    """Initializes the git helper.

    Arguments:
      project_path (str): the path to the git project folder.
    """
    super(GitHelper, self).__init__()
    self.project_path = project_path
    self._cwd = os.getcwd()

  def AddFileToTrack(self, file_path: str):
    """Add a file to those that are tracked by the git repo.

    Args:
      file_path (str): path to the file to be added to tracked
          files by this git repo.
    """
    command = 'git add {0:s}'.format(file_path)
    _, _, _ = self.RunCommand(command)

  def GetActiveBranch(self) -> str:
    """Determines the active branch of the git project.

    Returns:
      str: the active branch of the git project.

    Raises:
      errors.UnableToConfigure: when the tool is not able to get
          the active branch of the git project.
    """
    command = 'git branch --list --no-color'
    exit_code, output, error = self.RunCommand(command)

    if exit_code != 0:
      raise errors.UnableToConfigure((
          'Unable to get the active git branch, with error message '
          '{0:s}').format(error))

    for line in output.split('\n'):
      if line.startswith('*'):
        _, _, line_string = line.partition('*')
        return line_string.strip()
    raise errors.UnableToConfigure('Unable to determine the active git branch')

  def RunCommand(self, command: str) -> Tuple[int, str, str]:
    """Runs a command.

    Args:
      command (str): command to run.

    Returns:
      tuple[int, str, str]: exit code, output that was written to stdout
          and stderr.
    """
    os.chdir(self.project_path)
    exit_code, output, error = super(GitHelper, self).RunCommand(command)
    os.chdir(self._cwd)
    return exit_code, output, error

  def SwitchToBranch(self, branch: str) -> int:
    """Switches the git branch and returns the exit code of the command.

    Arguments:
      branch (str): the name of the git branch.

    Returns:
      int: the exit code from the git command.
    """
    command = 'git checkout {0:s}'.format(branch)
    exit_code, _, _ = self.RunCommand(command)

    return exit_code

  def CreateFeatureBranch(self, branch: str = '', module_name: str = ''):
    """Creates a feature branch in the git project.

    Arguments:
      branch (str): the name of the git branch.
      module_name (str): the name of the module. If module_name is present
          it will be used to construct the branch name, otherwise branch
          name will be used.

    Returns:
      str: the name of the created feature branch.

    Raises:
      errors.UnableToConfigure: when the tool is not able to create
          the feature branch of the git project.
    """
    if module_name:
      branch_name = re.sub('(?<!^)(?=[A-Z])', '_', module_name).lower()
    else:
      branch_name = branch

    if not branch_name:
      raise errors.UnableToConfigure('No branch name given.')

    active_branch = self.GetActiveBranch()
    if active_branch == branch_name:
      return branch_name

    command = 'git checkout -b {0:s}'.format(branch_name)
    exit_code, _, error = self.RunCommand(command)

    if exit_code != 0:
      raise errors.UnableToConfigure((
          'Unable to create the feature branch, with error message '
          '{0:s}').format(error))

    return branch_name
