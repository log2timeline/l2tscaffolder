# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test class for the scaffolder engine"""
import os
import unittest

from plasoscaffolder.lib import engine
from plasoscaffolder.lib import errors
from plasoscaffolder.plugins import interface as plugin_interface
from plasoscaffolder.projects import interface as project_interface
from plasoscaffolder.projects import manager as project_manager
from tests.test_helper import path_helper


class TestPluginOne(plugin_interface.ScaffolderPlugin):
  """Test plugin."""
  PROVIDES = 'Awesome'
  DESCRIPTION = 'This is a really awesome thing.'
  QUESTIONS = [
      plugin_interface.question('test1', 'a', 'b', str),
      plugin_interface.question('test2', 'a', 'b', str),
      plugin_interface.question('test3', 'a', 'b', str)]


class TestProject(project_interface.ScaffolderProject):
  """Plaso project definition."""

  PROJECT_TYPE = 'N/A'

  def ValidatePath(self, root_path: str) -> bool:
    """Validate a path to the test project."""
    if 'wrong' in root_path:
      return False

    if 'error' in root_path:
      return False

    return True


class ScaffolderEngineTest(unittest.TestCase):
  """Test case for the scaffolder engine functions. """

  @classmethod
  def setUpClass(cls):
    project_manager.ProjectManager.RegisterProject(TestProject)

  def testSetModuleName(self):
    """Test setting the module name."""
    eng = engine.ScaffolderEngine()
    test_name = 'foobar'

    eng.SetModuleName(test_name)

    module_name = getattr(eng, '_module_name', 'N/A')
    self.assertEqual(module_name, test_name.title())

    test_name = 'some module this is'
    expected_module_name = 'SomeModuleThisIs'
    expected_file_name = 'some_module_this_is'

    eng.SetModuleName(test_name)
    module_name = getattr(eng, '_module_name', 'N/A')
    file_name = getattr(eng, '_file_name_prefix', 'N/A')

    self.assertEquals(expected_module_name, module_name)
    self.assertEquals(expected_file_name, file_name)

  def testSetProjectRootPath(self):
    """Test setting the root path to a project."""
    eng = engine.ScaffolderEngine()

    # Test a path that will fail.
    path = os.path.join(os.path.curdir, 'wrong path')
    with self.assertRaises(errors.NoValidProject):
      eng.SetProjectRootPath(path)

    path = 'this is absolutely the correct path'
    eng.SetProjectRootPath(path)

    root_path = getattr(eng, '_project_root_path', '')
    project = getattr(eng, '_project', '')

    self.assertEqual(root_path, path)
    self.assertEqual(project, TestProject.PROJECT_TYPE)

  def testSetPlugin(self):
    """Test setting the plugin of a scaffolder engine."""
    eng = engine.ScaffolderEngine()
    test_plugin = TestPluginOne()

    eng.SetPlugin(test_plugin)

    self.assertTrue(hasattr(eng, '_plugin'))
    self.assertIsInstance(
        getattr(eng, '_plugin', None), plugin_interface.ScaffolderPlugin)

  def testStorePluginAttribute(self):
    """Test storing attributes in a plugin."""
    eng = engine.ScaffolderEngine()
    test_plugin = TestPluginOne()
    eng.SetPlugin(test_plugin)

    test_string1 = 'Test String'
    test_string2 = 'Part of the plugin'
    test_string3 = 'I\'m stored in the plugin!'

    eng.StorePluginAttribute('test1', test_string1, str)
    test, _ = test_plugin.IsPluginConfigured()
    self.assertFalse(test)
    eng.StorePluginAttribute('test2', test_string2, str)
    test, _ = test_plugin.IsPluginConfigured()
    self.assertFalse(test)
    eng.StorePluginAttribute('test3', test_string3, str)
    test, _ = test_plugin.IsPluginConfigured()
    self.assertTrue(test)

    plugin_attributes = getattr(test_plugin, '_attributes', {})
    test1_attr = plugin_attributes.get('test1', '')
    test2_attr = plugin_attributes.get('test2', '')
    test3_attr = plugin_attributes.get('test3', '')

    self.assertEqual(test1_attr, test_string1)
    self.assertEqual(test2_attr, test_string2)
    self.assertEqual(test3_attr, test_string3)


if __name__ == '__main__':
  unittest.main()
