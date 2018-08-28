# -*- coding: utf-8 -*-
"""The plaso project class."""

import os

from plasoscaffolder.lib import definitions
from plasoscaffolder.projects import interface
from plasoscaffolder.projects import manager

class PlasoProject(interface.ScaffolderProject):
  """Plaso project definition."""

  PROJECT_TYPE = definitions.PROJECT_PLASO

  def ValidatePath(self, root_path: str) -> bool:
    """Validate the path to the root directory.

    Args:
      root_path (str): the path to the root of the project directory.

    Returns:
      (bool): determines whether the given path is the correct root path
              of the project.
    """
    if not os.path.isdir(root_path):
      return False

    if not os.path.isdir(os.path.join(root_path, 'plaso')):
      return False

    if not os.path.isfile(os.path.join(root_path, 'plaso.ini')):
      return False

    if not os.path.isdir(os.path.join(root_path, 'plaso', 'parsers')):
      return False

    return True


manager.ProjectManager.RegisterProject(PlasoProject)
