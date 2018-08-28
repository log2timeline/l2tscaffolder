# -*- coding: utf-8 -*-
"""The scaffolder engine."""
import os

from plasoscaffolder.lib import definitions
from plasoscaffolder.lib import errors
from plasoscaffolder.lib import file_handler
from plasoscaffolder.plugins import interface as plugin_interface
from plasoscaffolder.projects import manager as project_manager

from typing import Generator
from typing import List
from typing import Type
from typing import Tuple


class ScaffolderEngine(object):
  """The engine, responsible for file handling and setting up plugins."""

  def __init__(self):
    """Initialize the engine."""
    super(ScaffolderEngine, self).__init__()
    self._attributes = {}
    self._file_handler = file_handler.FileHandler()
    self._module_name = ''
    self._file_name_prefix = ''
    self._plugin = None
    self._project = ''
    self._project_root_path = ''

  def _IsReadyToGenerate(self) -> Tuple[bool, str]:
    """Check to see if all attributes are set to start generating files.

    Returns:
      bool: Boolean indicating whether or not the plugin is fully configured.
      str: If the plugin is not fully configured the second value is a string
           that contains the reason why it is not fully configured.
    """
    if not self._project_root_path:
      return False, 'The path to the project root is not properly configured.'

    if not self._module_name:
      return False, 'Module name has not been configured.'

    if not self._plugin:
      return False, 'Plugin object not yet set.'

    return self._plugin.IsPluginConfigured()

  def GenerateFiles(self) -> List[str]:
    """Generates the needed files.

    Raises:
      PluginNotConfigured: When not all attributes have been configured.

    Returns:
      list: a list of all filenames that were generated and written to disk.
    """
    is_ready, reason = self._IsReadyToGenerate()
    if not is_ready:
      raise errors.PluginNotConfigured(reason)

    self._plugin.SetOutputName(self._file_name_prefix)

    written_files = []
    for file_source, file_destination in self._plugin.GetFilesToCopy():
      if os.path.isfile(file_source):
        full_path = os.path.join(self._project_root_path, file_destination)
        written_files.append(
            self._file_handler.CopyFile(file_source, full_path))

    for file_path, content in self._plugin.GenerateFiles():
      full_path = os.path.join(self._project_root_path, file_path)
      written_files.append(self._file_handler.AddContent(full_path, content))

    return written_files

  def SetModuleName(self, module_name: str):
    """Sets the module name as chosen by the user."""
    self._file_name_prefix = module_name.replace(' ', '_').lower()
    self._module_name = self._file_name_prefix.replace(
        '_', ' ').title().replace(' ', '')

  def SetPlugin(self, plugin: Type[plugin_interface.ScaffolderPlugin]):
    """Stores the plugin object in the engine."""
    self._plugin = plugin
    self._plugin.SetupPlugin()

  def SetProjectRootPath(self, root_path: str):
    """Set the path to the root of the project file.

    Raises:
      errors.NoValidProject: when root path is not identified as a valid project
                             path.
    """
    for project_object in project_manager.ProjectManager.GetProjectObjects():
      if project_object.ValidatePath(root_path):
        self._project = project_object.PROJECT_TYPE
        self._project_root_path = root_path
        return

    raise errors.NoValidProject('No valid project has been identified.')

  def StorePluginAttribute(self, name: str, value: object, value_type: object):
    """Store an attribute read from the CLI.

    Args:
      name (str): The attribute name.
      value (value_type): The attribute value.
      value_type (type): The attribute type.

    Raises:
      KeyError: If the attribute name is already defined.
      PluginNotConfigured: If the plugin has not yet been set.
      ValueError: If the value is not of the correct type.
    """
    if not self._plugin:
      raise errors.PluginNotConfigured(u'Plugin has not yet been set.')

    self._plugin.SetAttribute(name, value, value_type)
