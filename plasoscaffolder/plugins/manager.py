# -*- coding: utf-8 -*-
"""The plugin manager."""

from typing import Dict
from typing import List
from typing import Optional
from typing import Generator
from typing import Tuple
from typing import Type

from plasoscaffolder.plugins import interface


class PluginManager(object):
  """The plugin manager."""

  _plugin_classes = {}

  @classmethod
  def DeregisterPlugin(cls, plugin_class: Type[interface.ScaffolderPlugin]):
    """Deregisters a plugin class.

    The plugin classes are identified based on their lower case name.

    Args:
      plugin_class (type): plugin class (subclass of ScaffolderPlugin).

    Raises:
      KeyError: if plugin class is not set for the corresponding name.
    """
    plugin_provides = plugin_class.PROVIDES.lower()
    if plugin_provides not in cls._plugin_classes:
      raise KeyError('Plugin class not set for name: {0:s}.'.format(
          plugin_class.PROVIDES))

    del cls._plugin_classes[plugin_provides]

  @classmethod
  def GetPluginNames(cls) -> Generator[str, None, None]:
    """Retrieves the plugin names.

    Yields:
      str: plugin names.
    """
    for plugin_provides, plugin_class in cls.GetPlugins():
      yield plugin_provides

  @classmethod
  def GetPluginInformation(cls) -> Generator[Tuple[str, str], None, None]:
    """Retrieves the plugin information.

    Yields:
      tuple[str, str]: pairs of plugin names and descriptions.
    """
    for plugin_provides, plugin_class in cls.GetPlugins():
      description = getattr(plugin_class, 'DESCRIPTION', '')
      yield (plugin_provides, description)

  @classmethod
  def GetPluginObjectByProvides(cls, plugin_provides) -> Optional[interface.ScaffolderPlugin]:
    """Retrieves a specific plugin object by the parser it provides.

    Args:
      plugin_provides (str): name of the plugin or parser it provides.

    Returns:
      ScaffolderPlugin: plugin object or None.
    """
    plugin_class = cls._plugin_classes.get(plugin_provides.lower(), None)
    if plugin_class:
      return plugin_class()
    return None

  @classmethod
  def GetPluginObjects(cls) -> Dict[str, Type[interface.ScaffolderPlugin]]:
    """Retrieves the plugin objects.

    Returns:
      dict[str, ScaffolderPlugin]: plugins per name.
    """
    plugin_objects = {}
    for plugin_provides, plugin_class in iter(cls._plugin_classes.items()):
      plugin_object = plugin_class()
      plugin_objects[plugin_provides] = plugin_object

    return plugin_objects

  @classmethod
  def GetPluginQuestions(cls) -> List[List[str]]:
    """Retrieves all the questions asked by plugins."""
    questions = []
    for plugin_class in cls._plugin_classes.values():
      questions.extend(plugin_class.QUESTIONS)

    return questions

  @classmethod
  def GetPluginQuestionByName(cls, plugin_provides: str) -> list:
    """Retrieve a list of questions asked by a plugin based on name.

    Args:
      plugin_provides (str): name of the plugin or parser the plugin provides.

    Returns:
      list: a list with all the questions (namedtuple) needed to setup the
          plugin. If plugin_provides is not registered an empty list will
          be returned.
    """
    plugin_class = cls._plugin_classes.get(plugin_provides.lower(), None)
    if not plugin_class:
      return list()

    return plugin_class.QUESTIONS

  @classmethod
  def GetPlugins(cls):
    """Retrieves the registered plugins.

    Retrieves a dictionary of all registered plugins.

    Yields:
      tuple: contains:

      * str: name of the plugin:
      * type: plugin class (subclass of ScaffolderPlugin).
    """
    for plugin_provides, plugin_class in iter(cls._plugin_classes.items()):
      yield plugin_provides, plugin_class

  @classmethod
  def RegisterPlugin(cls, plugin_class: Type[interface.ScaffolderPlugin]):
    """Registers a plugin class.

    The plugin classes are identified based on their lower case name.

    Args:
      plugin_class (type): plugin class (subclass of ScaffolderPlugin).

    Raises:
      KeyError: if plugin class is already set for the corresponding name.
    """
    plugin_provides = plugin_class.PROVIDES.lower()
    if plugin_provides in cls._plugin_classes:
      raise KeyError('Plugin class already set for name: {0:s}.'.format(
          plugin_class.PROVIDES))

    cls._plugin_classes[plugin_provides] = plugin_class

  @classmethod
  def RegisterPlugins(cls, plugin_classes: List[Type[interface.ScaffolderPlugin]]):
    """Registers plugin classes.

    The plugin classes are identified based on their lower case name.

    Args:
      plugin_classes (list[type]): plugins classes
          (subclasses of ScaffolderPlugin).

    Raises:
      KeyError: if plugin class is already set for the corresponding name.
    """
    for plugin_class in plugin_classes:
      cls.RegisterPlugin(plugin_class)
