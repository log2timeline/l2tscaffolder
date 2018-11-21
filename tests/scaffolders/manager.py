# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the scaffolder manager."""
import unittest

from l2tscaffolder.scaffolders import interface
from l2tscaffolder.scaffolders import manager


class BaseScaffolderTest(interface.Scaffolder):
  """Basic class to inherit in tests."""

  def GenerateFiles(self):
    """Empty file generator."""

  def GetFilesToCopy(self):
    """Empty files to copy."""


class AwesomeTestScaffolder(BaseScaffolderTest):
  """First test scaffolder."""
  NAME = 'Awesome'
  DESCRIPTION = 'This is a really awesome thing.'
  QUESTIONS = [
      interface.StringQuestion('test1', 'enter the test'),
      interface.StringQuestion('test2', 'enter the test'),
      interface.StringQuestion('test3', 'enter the test')]


class AverageTestScaffolder(BaseScaffolderTest):
  """Second test scaffolder."""
  NAME = 'Average'
  DESCRIPTION = 'This scaffolder implements the average parser.'
  QUESTIONS = [
      interface.StringQuestion('mediocre', 'a'),
      interface.StringQuestion('lala', 'a'),
      interface.StringQuestion('ok', 'enter')]


class RegistrationTestScaffolder(BaseScaffolderTest):
  """Third test scaffolder."""
  NAME = 'Registration'
  DESCRIPTION = (
      'This scaffolder implements the registration scaffolder, required '
      'paperwork for many ISO standards of the future.')
  QUESTIONS = [
      interface.StringQuestion('27001', 'a'),
      interface.StringQuestion('9001', 'a'),
      interface.StringQuestion('3120512', 'a'),
      interface.ListQuestion('9001-2', 'enter the list here'),
      interface.StringQuestion('12362323', 'a')]


class NotAwesomeTestScaffolder(AwesomeTestScaffolder):
  """Test scaffolder for the Register function."""
  NAME = 'Clearly not awesome'


class ScaffolderManagerTest(unittest.TestCase):
  """Test class for the scaffolder manager."""

  @classmethod
  def setUpClass(cls):
    """Setup tests by registering three scaffolders and removing all others."""
    scaffolders = list(manager.ScaffolderManager.GetScaffolderClasses())
    for scaffolder in scaffolders:
      manager.ScaffolderManager.DeregisterScaffolder(scaffolder)

    manager.ScaffolderManager.RegisterScaffolders(
        [AwesomeTestScaffolder, AverageTestScaffolder,
         RegistrationTestScaffolder])

  def testDeregisterScaffolder(self):
    """Testing whether we can remove a scaffolder from the registration."""
    number_of_scaffolders = len(
        list(manager.ScaffolderManager.GetScaffolders()))
    self.assertEqual(number_of_scaffolders, 3)

    manager.ScaffolderManager.DeregisterScaffolder(AwesomeTestScaffolder)
    number_of_scaffolders = len(
        list(manager.ScaffolderManager.GetScaffolders()))
    self.assertEqual(number_of_scaffolders, 2)

    with self.assertRaises(KeyError):
      manager.ScaffolderManager.DeregisterScaffolder(NotAwesomeTestScaffolder)

    # Let's register it again for other tests to succeed.
    manager.ScaffolderManager.RegisterScaffolder(AwesomeTestScaffolder)

  def testGetScaffolderNames(self):
    """Testing the scaffolder names."""
    scaffolder_names = list(manager.ScaffolderManager.GetScaffolderNames())
    self.assertEqual(len(scaffolder_names), 3)

    correct_names = set(['awesome', 'average', 'registration'])
    scaffolder_name_set = set(scaffolder_names)

    self.assertSetEqual(correct_names, scaffolder_name_set)

  def testGetScaffolderInformation(self):
    """Testing the scaffolder information gathering of the manager."""
    scaffolder_description = {}
    for name, desc in manager.ScaffolderManager.GetScaffolderInformation():
      scaffolder_description[name] = desc

    self.assertEqual(len(scaffolder_description.keys()), 3)

    self.assertEqual(
        scaffolder_description.get('awesome', None),
        'This is a really awesome thing.')

    self.assertEqual(
        scaffolder_description.get('average', None),
        'This scaffolder implements the average parser.')

  def testGetScaffolderObjectByName(self):
    """Testing getting the scaffolder object by name."""
    scaffolder = manager.ScaffolderManager.GetScaffolderObjectByName(
        RegistrationTestScaffolder.NAME)

    self.assertEqual(scaffolder.NAME, RegistrationTestScaffolder.NAME)

  def testGetScaffolderObjects(self):
    """Testing scaffolder objects."""
    scaffolder_objects = manager.ScaffolderManager.GetScaffolderObjects()
    self.assertEqual(len(scaffolder_objects), 3)

    attributes = [
        scaffolder.NAME.lower() for scaffolder in scaffolder_objects.values()]
    correct = ['awesome', 'average', 'registration']

    self.assertSetEqual(set(attributes), set(correct))

  def testGetScaffolderQuestions(self):
    """Test getting all scaffolder questions."""
    questions = manager.ScaffolderManager.GetScaffolderQuestions()
    question_count = len(AwesomeTestScaffolder.QUESTIONS)
    question_count += len(AverageTestScaffolder.QUESTIONS)
    question_count += len(RegistrationTestScaffolder.QUESTIONS)

    self.assertEqual(question_count, len(questions))

    question_attributes = [x.attribute for x in questions]

    self.assertIn('test1', question_attributes)
    self.assertIn('lala', question_attributes)
    self.assertIn('27001', question_attributes)

  def testGetScaffolderQuestionByName(self):
    """Test fetching questions of a scaffolder scaffolder by NAME attribute."""
    questions = manager.ScaffolderManager.GetScaffolderQuestionByName(
        'registration')

    self.assertEqual(len(questions), 5)

    question_attributes = [question.attribute for question in questions]
    self.assertIn('27001', question_attributes)

  def testGetScaffolders(self):
    """Test getting scaffolders from the manager."""
    scaffolders = dict(list(manager.ScaffolderManager.GetScaffolders()))

    self.assertEqual(len(scaffolders.keys()), 3)
    correct = ['awesome', 'average', 'registration']
    self.assertEqual(set(scaffolders.keys()), set(correct))

  def testRegisterScaffolder(self):
    """Test registering new scaffolders."""
    with self.assertRaises(KeyError):
      manager.ScaffolderManager.RegisterScaffolder(AverageTestScaffolder)

    self.assertEqual(
        len(list(manager.ScaffolderManager.GetScaffolderNames())), 3)
    manager.ScaffolderManager.RegisterScaffolder(NotAwesomeTestScaffolder)
    scaffolder_names = list(manager.ScaffolderManager.GetScaffolderNames())
    self.assertEqual(len(scaffolder_names), 4)
    self.assertIn('clearly not awesome', scaffolder_names)
    manager.ScaffolderManager.DeregisterScaffolder(NotAwesomeTestScaffolder)

  def testRegisterScaffolders(self):
    """Test registering multiple scaffolders."""
    scaffolders = [
        AwesomeTestScaffolder, AverageTestScaffolder,
        RegistrationTestScaffolder]
    for scaffolder in scaffolders:
      manager.ScaffolderManager.DeregisterScaffolder(scaffolder)

    number_of_scaffolder_names = len(
        list(manager.ScaffolderManager.GetScaffolderNames()))
    self.assertEqual(number_of_scaffolder_names, 0)

    manager.ScaffolderManager.RegisterScaffolders(scaffolders)
    number_of_scaffolder_names = len(
        list(manager.ScaffolderManager.GetScaffolderNames()))
    self.assertEqual(number_of_scaffolder_names, 3)


if __name__ == '__main__':
  unittest.main()
