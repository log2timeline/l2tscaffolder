# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Project definitions used for testing purposes."""
from plasoscaffolder.projects import interface


class TestProject(interface.ScaffolderDefinition):
  """Test project."""

  NAME = 'stranger'

  def ValidatePath(self, root_path: str) -> bool:
    """Test validation."""
    if 'gold' in root_path:
      return True

    return False


class SecondTestProject(interface.ScaffolderDefinition):
  """Test project."""

  NAME = 'danger'

  def ValidatePath(self, root_path: str) -> bool:
    """Test validation."""
    if 'silver' in root_path:
      return True

    return False


class TestProjectFails(interface.ScaffolderDefinition):
  """Test project that always fails."""

  NAME = 'failing'

  def ValidatePath(self, root_path: str) -> bool:
    """Test validation."""
    return False


