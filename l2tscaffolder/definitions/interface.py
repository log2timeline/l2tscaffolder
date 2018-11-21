# -*- coding: utf-8 -*-
"""Interface defining how a project class looks like."""
import abc

from l2tscaffolder.lib import definitions

class ScaffolderDefinition:
  """Scaffolder definition interface."""

  NAME = definitions.DEFINITION_UNDEFINED

  @abc.abstractmethod
  def ValidatePath(self, root_path: str) -> bool:
    """Validates the path to the root directory of the project.

    Args:
      root_path (str): the path to the root of the project directory.

    Returns:
      bool: whether the given path is the correct root path of the project.
    """
