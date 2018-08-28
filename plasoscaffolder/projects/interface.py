# -*- coding: utf-8 -*-
"""Interface defining how a project class looks like."""
import abc

from plasoscaffolder.lib import definitions

class ScaffolderDefinition(object):
  """Scaffolder definition interface."""

  NAME = definitions.DEFINITION_UNDEFINED

  @abc.abstractmethod
  def ValidatePath(self, root_path: str) -> bool:
    """Validate the path to the root directory.

    Args:
      root_path (str): the path to the root of the project directory.

    Returns:
      (bool): determines whether the given path is the correct root path
              of the project.
    """
