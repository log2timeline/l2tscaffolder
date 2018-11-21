# !/usr/bin/python
# -*- coding: utf-8 -*-
"""The scaffolder frontend."""
import os
from typing import Dict
from typing import List

from l2tscaffolder.frontend import output_handler as handler
from l2tscaffolder.helpers import git
from l2tscaffolder.lib import engine
from l2tscaffolder.lib import errors

from l2tscaffolder.definitions import interface as definition_interface
from l2tscaffolder.definitions import manager as definition_manager
from l2tscaffolder.scaffolders import interface as scaffolder_interface
from l2tscaffolder.scaffolders import manager as scaffolder_manager


class ScaffolderFrontend:
  """A frontend implementation for the scaffolder project."""

  def __init__(self, output_handler: handler.BaseOutputHandler):
    """Initializes the frontend.

    Args:
      output_handler (handler.BaseOutputHandler): the output handler used
          for the frontend.
    """
    self._git_helper = None
    self._output_handler = output_handler

  def _AskDictQuestion(
      self, question: scaffolder_interface.DictQuestion) -> Dict[str, str]:
    """Prompts the user with a question and return a dict answer back.

    The user is prompted to supply both the key and value for each
    entry in the dict. The key is the first response from the user and
    value the second one. If the user attempts to add an entry with a key
    that already exists an error is presented to the user and they are asked
    to try again.

    Args:
      question (scaffolder_interface.DictQuestion): the question to ask.

    Returns:
      dict[str, str]: keys and values provided by the user.
    """
    return_dict = {}

    more_entries = True
    entry_index = 1
    while more_entries:
      key = self._output_handler.PromptInfo(
          '{0:s} [#{1:d}]'.format(question.key_prompt, entry_index))
      if key in return_dict:
        self._output_handler.PrintError(
            'Key value ({0:s}) already entered.'.format(key))
        continue

      value = self._output_handler.PromptInfo(
          '{0:s} [#{1:d}]'.format(question.value_prompt, entry_index))

      return_dict[key] = value
      more_entries = self._output_handler.Confirm('More entries?', abort=False)
      entry_index += 1

    question.ValidateAnswer(return_dict)
    return return_dict

  def _AskListQuestion(
      self, question: scaffolder_interface.ListQuestion) -> List[str]:
    """Prompts the user with a question and return a list back.

    Args:
      question (scaffolder_interface.ListQuestion): the question to ask.

    Returns:
      list: the answer as supplied by the user.
    """
    return_list = []

    more_entries = True
    entry_index = 1
    while more_entries:
      value = self._output_handler.PromptInfo(
          'Value to add [#{0:d}]'.format(entry_index))
      if not value:
        self._output_handler.PrintError('Empty value, not adding.')
      else:
        return_list.append(value)

      more_entries = self._output_handler.Confirm(
          'Add more values?', abort=False)
      entry_index += 1

    question.ValidateAnswer(return_list)
    return return_list

  def _AskQuestion(self, question: scaffolder_interface.BaseQuestion) -> object:
    """Prompts the user with a question and return an answer back.

    Args:
      question (scaffolder_interface.BaseQuestion): the question to ask.

    Returns:
      object: an object, whose type is defined by the question.

    Raises:
      errors.WrongCliInput: when an unsupported question type is
          encountered.
    """
    self._output_handler.PrintNewLine()
    self._output_handler.PrintInfo(question.prompt)

    if isinstance(question, scaffolder_interface.StringQuestion):
      return self._AskStringQuestion(question)

    if isinstance(question, scaffolder_interface.DictQuestion):
      return self._AskDictQuestion(question)

    if isinstance(question, scaffolder_interface.ListQuestion):
      return self._AskListQuestion(question)

    # TODO: Add support for other types of questions.
    raise errors.WrongCliInput(
        'Question type {0:s} not supported.'.format(str(question.__class__)))

  def _AskStringQuestion(
      self, question: scaffolder_interface.StringQuestion) -> str:
    """Prompts the user with a question and return a string answer back.

    Args:
      question (scaffolder_interface.StringQuestion): the question to ask.

    Returns:
      str: the answer as supplied by the user.
    """
    value = self._output_handler.PromptInfo('Value')
    question.ValidateAnswer(value)
    return value

  def _GetSelection(self, items: list, item_text: str) -> str:
    """Presents a list of strings to user and return back user choice.

    Args:
      items (list): list of strings to present to the user.
      item_text (str): heading used in presentation to the user.

    Returns:
      str: the chosen string from the list.

    Raises:
      KeyError: if the user selection is not part of the list or
          it's not a valid number.
    """
    for item_count, item in enumerate(items):
      self._output_handler.PrintInfo(
          '  [{0:d}] {1:s}'.format(item_count, item))

    result = self._output_handler.PromptInfo('{0:s} choice'.format(item_text))
    try:
      result_int = int(result, 10)

      if 0 <= result_int < len(items):
        return items[result_int]
    except ValueError:
      raise KeyError('Unable to convert {0:s} into a number.'.format(result))

    raise KeyError(
        'Item [{0:d}] not in list, please pick a valid number.'.format(
            result_int))

  def CreateGitFeatureBranch(self, project_path: str, module_name: str):
    """Creates a feature branch inside the git project.

    Creates a feature branch inside the git project path
    to store all the generated files in.

    Args:
      project_path (str): path to the git project folder.
      module_name (str): name of the output module.
    """
    branch_name = self._git_helper.GenerateBranchName(module_name)
    if not self._git_helper.HasBranch(branch_name):
      self._output_handler.PrintOutput(
          'Creating feature branch: {0:s} inside {1:s}'.format(
              branch_name, project_path))
      self._git_helper.CreateBranch(branch_name)

    self._output_handler.PrintOutput('Switching to feature branch {0:s}'.format(
        branch_name))
    self._git_helper.SwitchToBranch(branch_name)

  def GatherScaffolderAnswers(self, scaffolder, scaffolder_engine):
    """Asks all questions that scaffolder requires and store the results in it.

    Args:
      scaffolder (scaffolder_interface.Scaffolder): the scaffolder that
          stores all required questions and stores all results as well.
      scaffolder_engine (scaffolder_engine.ScaffolderEngine): the scaffolder
          engine object, needed to store answers from questions asked.

    Raises:
      UnableToConfigure: if the answer causes the scaffolder not
          to be configured properly.
    """
    for question in scaffolder.GetQuestions():
      gather_answer = True
      # Loop created to give the user a chance to correct each incorrect
      # answer they provide.
      while gather_answer:
        try:
          value = self._AskQuestion(question)
          scaffolder_engine.StoreScaffolderAttribute(
              question.attribute, value, question.TYPE)
          break
        except errors.UnableToConfigure as exception:
          self._output_handler.PrintError(
              'Unable to configure, with error: {0:s}'.format(repr(exception)))
          gather_answer = self._output_handler.Confirm('Want to try again?')
          if not gather_answer:
            raise

  def GetDefinition(
      self,
      definition_string: str) -> definition_interface.ScaffolderDefinition:
    """Returns the definition object as chosen by the user.

    Args:
      definition_string (str): definition name, read from user input.

    Returns:
      definition_interface.ScaffolderDefinition: the chosen definition object.
    """
    definitions = list(
        definition_manager.DefinitionManager.GetDefinitionNames())

    self._output_handler.PrintNewLine()
    if not definition_string:
      self._output_handler.PrintInfo('Available definitions: ')
      definition_string = ''
      while not definition_string:
        try:
          definition_string = self._GetSelection(definitions, 'Definition')
        except KeyError as e:
          self._output_handler.PrintError('{0!s}'.format(e))

    if definition_string in definitions:
      self._output_handler.PrintOutput(
          '{0:s} chosen.'.format(definition_string))
      def_class = definition_manager.DefinitionManager.GetDefinitionByName(
          definition_string)
      return def_class()

    self._output_handler.PrintError(
        'Definition {0:s} does not exist.'.format(definition_string))
    return self.GetDefinition('')

  def GetModuleName(self) -> str:
    """Returns the module name as chosen by the user."""
    self._output_handler.PrintNewLine()
    self._output_handler.PrintInfo((
        'Name of the module to be generated. This can be something like "'
        'foobar sqlite" or "event analytics".\n\nThis will be used for class '
        'name generation and file name prefixes.'))
    return self._output_handler.PromptInfo('Module Name')

  def GetProjectPath(
      self, definition: definition_interface.ScaffolderDefinition) -> str:
    """Returns the path to the project's root folder as chosen by the user.

    Args:
      definition (definition_interface.ScaffolderDefinition): the chosen
          definition. Used to validate the project path.

    Returns:
      str: the path to the project's root folder.

    Raises:
      errors.WrongCliInput: when no valid project path has been provided.
    """
    self._output_handler.PrintNewLine()
    project_path = self._output_handler.PromptInfo('Path to the project root')
    if definition.ValidatePath(project_path):
      self._output_handler.PrintOutput(
          'Path [{0:s}] set as the project path.'.format(project_path))
      self._git_helper = git.GitHelper(project_path)
      return project_path

    check = self._output_handler.Confirm((
        'Path [{0:s}] does not lead to a valid project for {1:s}. '
        'Do you want to try again?').format(project_path, definition.NAME))

    if check:
      return self.GetProjectPath(definition)

    raise errors.WrongCliInput(
        'Unable to proceed without a valid project path.')

  def GetScaffolder(
      self, definition: definition_interface.ScaffolderDefinition
  ) -> scaffolder_interface.Scaffolder:
    """Returns the scaffolder as chosen by the user.

    Args:
      definition (definition_interface.ScaffolderDefinition): the chosen
          definition. Used to determine available scaffolders.

    Returns:
      scaffolder_interface.ScaffolderCli: the chosen scaffolder object.
    """
    scaffolders = {}
    manager = scaffolder_manager.ScaffolderManager
    for scaffolder_name, scaffolder in manager.GetScaffolders():
      if scaffolder.PROJECT == definition.NAME:
        scaffolders[scaffolder_name] = scaffolder

    self._output_handler.PrintNewLine()
    self._output_handler.PrintInfo(
        'Available scaffolders for {0:s}:'.format(definition.NAME))

    scaffolder = ''
    while not scaffolder:
      try:
        scaffolder = self._GetSelection(list(scaffolders.keys()), 'Scaffolder')
      except KeyError as exception:
        self._output_handler.PrintError('{0!s}'.format(exception))
    if scaffolder in scaffolders:
      return scaffolders[scaffolder]()

    self._output_handler.PrintError(
        'Scaffolder: {0:s} does not exist.'.format(scaffolder))
    return self.GetScaffolder(definition)

  def Start(self, definition_value):
    """Start the CLI.

    Args:
      definition_value (str): the definition string chosen by UI.
    """
    self._output_handler.PrintInfo('   == Starting the scaffolder ==')
    self._output_handler.PrintInfo('Gathering required information.')
    scaffolder_engine = engine.ScaffolderEngine()

    definition = self.GetDefinition(definition_value)

    project_path = self.GetProjectPath(definition)
    scaffolder_engine.SetProjectRootPath(project_path)

    module_name = self.GetModuleName()
    scaffolder_engine.SetModuleName(module_name)
    self._output_handler.PrintInfo(
        'About to create a new feature branch to store newly generated code.')
    try:
      self.CreateGitFeatureBranch(project_path, scaffolder_engine.module_name)
    except errors.UnableToConfigure as exception:
      self._output_handler.PrintError((
          'Unable to create feature branch, is {0:s} a valid git project path? '
          'The error message was: {1!s}').format(project_path, exception))
      self._output_handler.PrintError('Due to fatal error, not proceeding.')
      return

    scaffolder = self.GetScaffolder(definition)
    scaffolder_engine.SetScaffolder(scaffolder)
    try:
      self.GatherScaffolderAnswers(scaffolder, scaffolder_engine)
    except errors.UnableToConfigure as exception:
      self._output_handler.PrintError(
          ('Aborting. Unable to properly configure scaffolder '
           'with error {0!s}.').format(exception))
      return

    ready = self._output_handler.Confirm('Ready to generate files?')
    if ready:
      for file_path in scaffolder_engine.GenerateFiles():
        self._output_handler.PrintOutput(
            'File: {0:s} written to disk.'.format(file_path))
        _, _, file_path_inside_project = file_path.partition(project_path)
        if file_path_inside_project.startswith(os.sep):
          file_path_inside_project = file_path_inside_project[1:]
        self._git_helper.AddFileToTrack(file_path_inside_project)
