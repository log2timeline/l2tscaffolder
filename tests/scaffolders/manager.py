# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the scaffolder manager."""
import unittest

from plasoscaffolder.scaffolders import interface
from plasoscaffolder.scaffolders import manager


class TestScaffolderOne(interface.Scaffolder):
  """First test scaffolder."""
  NAME = 'Awesome'
  DESCRIPTION = 'This is a really awesome thing.'
  QUESTIONS = [
      interface.Question('test1', 'a', 'b', str),
      interface.Question('test2', 'a', 'b', str),
      interface.Question('test3', 'a', 'b', str)]


class TestScaffolderTwo(interface.Scaffolder):
  """Second test scaffolder."""
  NAME = 'Average'
  DESCRIPTION = 'This scaffolder implements the average parser.'
  QUESTIONS = [
      interface.Question('mediocre', 'a', 'b', str),
      interface.Question('lala', 'a', 'b', str),
      interface.Question('ok', 'a', 'b', str)]


class TestScaffolderThree(interface.Scaffolder):
  """Third test scaffolder."""
  NAME = 'Registration'
  DESCRIPTION = (
      'This scaffolder implements the registration scaffolder, required '
      'paperwork for many ISO standards of the future.')
  QUESTIONS = [
      interface.Question('27001', 'a', 'b', str),
      interface.Question('9001', 'a', 'b', str),
      interface.Question('3120512', 'a', 'b', str),
      interface.Question('12362323', 'a', 'b', str)]


class TestRegisterScaffolder(TestScaffolderOne):
  """Test scaffolder for the Register function."""
  NAME = 'Clearly not awesome'


class ScaffolderManagerTest(unittest.TestCase):
  """Test class for the scaffolder manager."""

  @classmethod
  def setUpClass(cls):
    """Setup the tests by registering three scaffolders."""
    manager.ScaffolderManager.RegisterScaffolders(
        [TestScaffolderOne, TestScaffolderTwo, TestScaffolderThree])

  def testDeregisterScaffolder(self):
    """Testing whether we can remove a scaffolder from the registration."""
    self.assertEqual(len(list(manager.ScaffolderManager.GetScaffolders())), 3)

    manager.ScaffolderManager.DeregisterScaffolder(TestScaffolderOne)
    self.assertEqual(len(list(manager.ScaffolderManager.GetScaffolders())), 2)

    with self.assertRaises(KeyError):
      manager.ScaffolderManager.DeregisterScaffolder(TestRegisterScaffolder)

    # Let's register it again for other tests to succeed.
    manager.ScaffolderManager.RegisterScaffolder(TestScaffolderOne)

  def testGetScaffolderNames(self):
    """Testing the scaffolder names."""
    scaffolder_names = list(manager.ScaffolderManager.GetScaffolderNames())
    self.assertEquals(len(scaffolder_names), 3)

    correct_names = set(['awesome', 'average', 'registration'])
    scaffolder_name_set = set(scaffolder_names)

    self.assertSetEqual(correct_names, scaffolder_name_set)

  def testGetScaffolderInformation(self):
    """Testing the scaffolder information gathering of the manager."""
    scaffolder_description = {}
    for name, description in manager.ScaffolderManager.GetScaffolderInformation():
      scaffolder_description[name] = description

    self.assertEqual(len(scaffolder_description.keys()), 3)

    self.assertEqual(
        scaffolder_description.get('awesome', None),
        'This is a really awesome thing.')

    self.assertEqual(
        scaffolder_description.get('average', None),
        'This scaffolder implements the average parser.')

  def testGetScaffolderObjectByName(self):
    """Testing getting the scaffolder object by name of provides."""
    scaffolder = manager.ScaffolderManager.GetScaffolderObjectByName(
        TestScaffolderThree.NAME)

    self.assertEqual(scaffolder.NAME, TestScaffolderThree.NAME)

  def testGetScaffolderObjects(self):
    """Testing scaffolder objects."""
    scaffolder_objects = manager.ScaffolderManager.GetScaffolderObjects()
    self.assertEquals(len(scaffolder_objects), 3)

    attributes = [x.NAME.lower() for x in scaffolder_objects.values()]
    correct = ['awesome', 'average', 'registration']

    self.assertSetEqual(set(attributes), set(correct))

  def testGetScaffolderQuestions(self):
    """Test getting all scaffolder questions."""
    questions = manager.ScaffolderManager.GetScaffolderQuestions()
    question_count = len(TestScaffolderOne.QUESTIONS)
    question_count += len(TestScaffolderTwo.QUESTIONS)
    question_count += len(TestScaffolderThree.QUESTIONS)

    self.assertEqual(question_count, len(questions))

    question_attributes = [x.attribute for x in questions]

    self.assertIn('test1', question_attributes)
    self.assertIn('lala', question_attributes)
    self.assertIn('27001', question_attributes)

  def testGetScaffolderQuestionByName(self):
    """Test fetching questions of a scaffolder scaffolder by NAME attribute."""
    reg_questions = manager.ScaffolderManager.GetScaffolderQuestionByName(
        'registration')

    self.assertEquals(len(reg_questions), 4)

    question_attributes = [x.attribute for x in reg_questions]
    self.assertIn('27001', question_attributes)

  def testGetScaffolders(self):
    """Test getting scaffolders from the manager."""
    scaffolders = dict(list(manager.ScaffolderManager.GetScaffolders()))

    self.assertEquals(len(scaffolders.keys()), 3)
    correct = ['awesome', 'average', 'registration']
    self.assertEquals(set(scaffolders.keys()), set(correct))

  def testRegisterScaffolder(self):
    """Test registering new scaffolders."""
    with self.assertRaises(KeyError):
      manager.ScaffolderManager.RegisterScaffolder(TestScaffolderTwo)

    self.assertEqual(
        len(list(manager.ScaffolderManager.GetScaffolderNames())), 3)
    manager.ScaffolderManager.RegisterScaffolder(TestRegisterScaffolder)
    scaffolder_names = list(manager.ScaffolderManager.GetScaffolderNames())
    self.assertEqual(len(scaffolder_names), 4)
    self.assertIn('clearly not awesome', scaffolder_names)
    manager.ScaffolderManager.DeregisterScaffolder(TestRegisterScaffolder)

  def testRegisterScaffolders(self):
    """Test registering multiple scaffolders."""
    scaffolders = [TestScaffolderOne, TestScaffolderTwo, TestScaffolderThree]
    for scaffolder in scaffolders:
      manager.ScaffolderManager.DeregisterScaffolder(scaffolder)

    self.assertEqual(
        len(list(manager.ScaffolderManager.GetScaffolderNames())), 0)
    manager.ScaffolderManager.RegisterScaffolders(scaffolders)
    self.assertEqual(
        len(list(manager.ScaffolderManager.GetScaffolderNames())), 3)


if __name__ == '__main__':
  unittest.main()
