# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Project definitions used for testing purposes."""
from plasoscaffolder.projects import interface


class TestProject(interface.ScaffolderProject):
  """Test project."""

  PROJECT_TYPE = 'stranger'

  def ValidatePath(self, root_path: str) -> bool:
    """Test validation."""
    if 'gold' in root_path:
      return True

    return False


class SecondTestProject(interface.ScaffolderProject):
  """Test project."""

  PROJECT_TYPE = 'danger'

  def ValidatePath(self, root_path: str) -> bool:
    """Test validation."""
    if 'silver' in root_path:
      return True

    return False


class TestProjectFails(interface.ScaffolderProject):
  """Test project that always fails."""

  PROJECT_TYPE = 'failing'

  def ValidatePath(self, root_path: str) -> bool:
    """Test validation."""
    return False


