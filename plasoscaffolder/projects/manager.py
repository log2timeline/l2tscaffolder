# -*- coding: utf-8 -*-
"""The project manager."""


from typing import Type

from plasoscaffolder.projects import interface


class ProjectManager(object):
  """The project manager."""

  _project_classes = {}

  @classmethod
  def DeregisterPlugin(cls, project_class: Type[interface.ScaffolderProject]):
    """Deregisters a project class.

    The project classes are identified based on their defined type.

    Args:
      project_class (type): project class (subclass of ScaffolderProject).

    Raises:
      KeyError: if project class is not set for the corresponding name.
    """
    project_type = project_class.PROJECT_TYPE

    if project_type not in cls._project_classes:
      raise KeyError('Project class not set for name: {0:s}.'.format(
          project_type))

    del cls._project_classes[project_type]

  @classmethod
  def GetProjectNames(cls):
    """Retrieves the project names.

    Yields:
      str: project names.
    """
    for project_provides in cls._project_classes:
      yield project_provides

  @classmethod
  def GetProjectObjects(cls) -> Type[interface.ScaffolderProject]:
    """Retrieves the project objects.

    Yields:
      ScaffolderProject: project object.
    """
    for project_class in cls._project_classes.values():
      project_object = project_class()
      yield project_object

  @classmethod
  def RegisterProject(cls, project_class: Type[interface.ScaffolderProject]):
    """Registers a project class.

    The project classes are identified based on their provided type.

    Args:
      project_class (ScaffolderProject): plugin class.

    Raises:
      KeyError: if project class is already set for the corresponding name.
    """
    project_type = project_class.PROJECT_TYPE

    if project_type in cls._project_classes:
      raise KeyError('Project class already set for name: {0:s}.'.format(
          project_type))

    cls._project_classes[project_type] = project_class
