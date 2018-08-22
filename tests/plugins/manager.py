# !/usr/bin/python
# -*- coding: utf-8 -*-
"""test class for the plugin manager."""
import collections
import unittest

from plasoscaffolder.plugins import interface
from plasoscaffolder.plugins import manager

class TestPluginOne(interface.ScaffolderPlugin):
  """First test plugin."""
  PROVIDES = 'Awesome'
  DESCRIPTION = 'This is a really awesome thing.'
  QUESTIONS = [
      interface.question('test1', 'a', 'b', str),
      interface.question('test2', 'a', 'b', str),
      interface.question('test3', 'a', 'b', str)]


class TestPluginTwo(interface.ScaffolderPlugin):
  """Second test plugin."""
  PROVIDES = 'Average'
  DESCRIPTION = 'This plugin implements the average parser.'
  QUESTIONS = [
      interface.question('mediocre', 'a', 'b', str),
      interface.question('lala', 'a', 'b', str),
      interface.question('ok', 'a', 'b', str)]


class TestPluginThree(interface.ScaffolderPlugin):
  """Third test plugin."""
  PROVIDES = 'Registration'
  DESCRIPTION = (
      'This plugin implements the registration plugin, required paperwork for '
      'many ISO standards of the future.')
  QUESTIONS = [
      interface.question('27001', 'a', 'b', str),
      interface.question('9001', 'a', 'b', str),
      interface.question('3120512', 'a', 'b', str),
      interface.question('12362323', 'a', 'b', str)]


class TestRegisterPlugin(TestPluginOne):
  """Test plugin for the Register function."""
  PROVIDES = 'Clearly not awesome'


class PluginManagerTest(unittest.TestCase):
  """Test class for the plugin manager."""

  @classmethod
  def setUpClass(cls):
    """Setup the tests by registering three plugins."""
    manager.PluginManager.RegisterPlugins(
        [TestPluginOne, TestPluginTwo, TestPluginThree])

  def testDeregisterPlugin(self):
    """Testing whether or not we can remove a plugin from the registration."""
    self.assertEqual(len(list(manager.PluginManager.GetPlugins())), 3)

    manager.PluginManager.DeregisterPlugin(TestPluginOne)
    self.assertEqual(len(list(manager.PluginManager.GetPlugins())), 2)

    with self.assertRaises(KeyError):
      manager.PluginManager.DeregisterPlugin(TestRegisterPlugin)

    # Let's register it again for other tests to succeed.
    manager.PluginManager.RegisterPlugin(TestPluginOne)

  def testGetPluginNames(self):
    """Testing the plugin names."""
    plugin_names = list(manager.PluginManager.GetPluginNames())
    self.assertEquals(len(plugin_names), 3)

    correct_names = set(['awesome', 'average', 'registration'])
    plugin_name_set = set(plugin_names)

    self.assertSetEqual(correct_names, plugin_name_set)

  
  def testGetPluginInformation(self):
    """Testing the plugin information gathering of the manager."""
    plugin_description = {}
    for name, description in manager.PluginManager.GetPluginInformation():
      plugin_description[name] = description

    self.assertEqual(len(plugin_description.keys()), 3)

    self.assertEqual(
        plugin_description.get('awesome', None),
        'This is a really awesome thing.')

    self.assertEqual(
        plugin_description.get('average', None),
        'This plugin implements the average parser.')

  def testGetPluginObjectByProvides(self):
    """Testing getting the plugin object by name of provides."""
    plugin = manager.PluginManager.GetPluginObjectByProvides(
        TestPluginThree.PROVIDES)

    self.assertEqual(plugin.PROVIDES, TestPluginThree.PROVIDES)

  def testGetPluginObjects(self):
    """Testing plugin objects."""
    objs = manager.PluginManager.GetPluginObjects().values()
    self.assertEquals(len(objs), 3)

    attributes = [x.PROVIDES.lower() for x in objs]
    correct = ['awesome', 'average', 'registration']

    self.assertSetEqual(set(attributes), set(correct))


  def testGetPluginQuestions(self):
    """Test getting all plugin questions."""
    questions = manager.PluginManager.GetPluginQuestions()
    question_count = len(TestPluginOne.QUESTIONS)
    question_count += len(TestPluginTwo.QUESTIONS)
    question_count += len(TestPluginThree.QUESTIONS)

    self.assertEqual(question_count, len(questions))

    question_attributes = [x.attribute for x in questions]

    self.assertIn('test1', question_attributes)
    self.assertIn('lala', question_attributes)
    self.assertIn('27001', question_attributes)

  def testGetPluginQuestionByName(self):
    """Test fetching a question by provides string."""
    reg_questions = manager.PluginManager.GetPluginQuestionByName(
        'registration')

    self.assertEquals(len(reg_questions), 4)

    question_attributes = [x.attribute for x in reg_questions]
    self.assertIn('27001', question_attributes)


  def testGetPlugins(self):
    """Test getting plugins from the manager."""
    plugins = dict(list(manager.PluginManager.GetPlugins()))

    self.assertEquals(len(plugins.keys()), 3)
    correct = ['awesome', 'average', 'registration']
    self.assertEquals(set(plugins.keys()), set(correct))

  def testRegisterPlugin(self):
    """Test registering new plugins."""
    with self.assertRaises(KeyError):
      manager.PluginManager.RegisterPlugin(TestPluginTwo)

    self.assertEqual(len(list(manager.PluginManager.GetPluginNames())), 3)
    manager.PluginManager.RegisterPlugin(TestRegisterPlugin)
    plugin_names = list(manager.PluginManager.GetPluginNames())
    self.assertEqual(len(plugin_names), 4)
    self.assertIn('clearly not awesome', plugin_names)
    manager.PluginManager.DeregisterPlugin(TestRegisterPlugin)

  def testRegisterPlugins(self):
    """Test registering mulitple plugins."""
    plugins = [TestPluginOne, TestPluginTwo, TestPluginThree]
    for plugin in plugins:
      manager.PluginManager.DeregisterPlugin(plugin)

    self.assertEqual(len(list(manager.PluginManager.GetPluginNames())), 0)
    manager.PluginManager.RegisterPlugins(plugins)
    self.assertEqual(len(list(manager.PluginManager.GetPluginNames())), 3)


if __name__ == '__main__':
  unittest.main()
