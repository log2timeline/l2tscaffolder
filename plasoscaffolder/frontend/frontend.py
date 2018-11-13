# !/usr/bin/python
# -*- coding: utf-8 -*-
"""The scaffolder frontend."""
import os
from typing import Dict
from typing import List
from typing import Type

from plasoscaffolder.frontend import output_handler
from plasoscaffolder.helpers import git
from plasoscaffolder.lib import engine
from plasoscaffolder.lib import errors

from plasoscaffolder.definitions import interface as definition_interface
from plasoscaffolder.definitions import manager as definition_manager
from plasoscaffolder.scaffolders import interface as scaffolder_interface
from plasoscaffolder.scaffolders import manager as scaffolder_manager


class ScaffolderFrontend:
  """A frontend implementation for the scaffolder project."""

  _git_helper = None
  _OUTPUT_HANDLER = output_handler.BaseOutputHandler()

  @classmethod
  def _AskDictQuestion(
      cls, question: scaffolder_interface.DictQuestion) -> Dict[str, str]:
    """Prompts the user with a question and return a dict answer back.

    Args:
      question (scaffolder_interface.DictQuestion): the question to ask.

    Returns:
      dict: the answer as supplied by the user. The user is prompted with
          questions to both supply the key and value to each entry in the
          dict. Key is chosen as the first response from the user and value
          as the second one. If the user attempts to add an entry with a key
          that already exists an error is presented to the user and they asked
          to try again (addition is rejected if key already exists).
    """
    return_dict = {}

    more_entries = True
    entry_index = 1
    while more_entries:
      # pylint: disable=assignment-from-no-return
      key = cls._OUTPUT_HANDLER.PromptInfo(
          '{0:s} [#{1:d}]'.format(question.key_prompt, entry_index))
      if key in return_dict:
        cls._OUTPUT_HANDLER.PrintError(
            'Key value ({0:s}) already entered.'.format(key))
        continue

      value = cls._OUTPUT_HANDLER.PromptInfo(
          '{0:s} [#{1:d}]'.format(question.value_prompt, entry_index))

      return_dict[key] = value
      more_entries = cls._OUTPUT_HANDLER.Confirm('More entries?', abort=False)
      entry_index += 1

    question.ValidateAnswer(return_dict)
    return return_dict

  @classmethod
  def _AskListQuestion(
      cls, question: scaffolder_interface.ListQuestion) -> List[str]:
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
      # pylint: disable=assignment-from-no-return
      value = cls._OUTPUT_HANDLER.PromptInfo(
          'Value to add [#{0:d}]'.format(entry_index))
      if not value:
        cls._OUTPUT_HANDLER.PrintError('Empty value, not adding.')
      else:
        return_list.append(value)

      more_entries = cls._OUTPUT_HANDLER.Confirm(
          'Add more values?', abort=False)
      entry_index += 1

    question.ValidateAnswer(return_list)
    return return_list

  @classmethod
  def _AskQuestion(cls, question: scaffolder_interface.BaseQuestion) -> Type:
    """Prompts the user with a question and return an answer back.

    Args:
      question (scaffolder_interface.BaseQuestion): the question to ask.

    Returns:
      object: an object, whos type is defined in question.type.

    Raises:
      errors.WrongCliInput: when an unsupported question type is
          encountered.
    """
    cls._OUTPUT_HANDLER.PrintNewLine()
    cls._OUTPUT_HANDLER.PrintInfo(question.prompt)

    if question.TYPE == str:
      return cls._AskStringQuestion(question)

    if question.TYPE == dict:
      return cls._AskDictQuestion(question)

    if question.TYPE == list:
      return cls._AskListQuestion(question)

    # TODO: Add support for other types of questions.
    raise errors.WrongCliInput(
        'Question type {0:s} not supported.'.format(str(question.TYPE)))

  @classmethod
  def _AskStringQuestion(
      cls, question: scaffolder_interface.StringQuestion) -> str:
    """Prompts the user with a question and return a string answer back.

    Args:
      question (scaffolder_interface.StringQuestion): the question to ask.

    Returns:
      str: the answer as supplied by the user.
    """
    # pylint: disable=assignment-from-no-return
    value = cls._OUTPUT_HANDLER.PromptInfo('Value')
    question.ValidateAnswer(value)
    return value

  @classmethod
  def _GetSelection(cls, items: list, item_text: str) -> str:
    """Present a list of strings to user and return back user choice.

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
      cls._OUTPUT_HANDLER.PrintInfo(
          '  [{0:d}] {1:s}'.format(item_count + 1, item))

    # pylint: disable=assignment-from-no-return
    result = cls._OUTPUT_HANDLER.PromptInfo('{0:s} choice'.format(item_text))
    try:
      result_int = int(result, 10)

      if result_int <= len(items):
        return items[result_int - 1]
    except ValueError:
      raise KeyError('Unable to convert {0:s} into a number.'.format(result))

    raise KeyError(
        'Item [{0:d}] not in list, please pick a valid number.'.format(
            result_int))

  @classmethod
  def CreateGitFeatureBranch(cls, project_path: str, module_name: str):
    """Create a feature branch inside the git project.

    Creates a feature branch inside the git project path
    to store all the generated files in.

    Args:
      project_path (str): path to the git project folder.
      module_name (str): name of the output module.
    """
    branch_name = cls._git_helper.CreateFeatureBranch(module_name=module_name)
    cls._OUTPUT_HANDLER.PrintOutput(
        'Created the feature branch: {0:s} inside {1:s}'.format(
            branch_name, project_path))

  @classmethod
  def GatherScaffolderAnswers(cls, scaffolder, scaffolder_engine):
    """Ask all questions that scaffolder requires and store the results in it.

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
          value = cls._AskQuestion(question)
          break
        except errors.UnableToConfigure as exception:
          # pylint: disable=assignment-from-no-return
          cls._OUTPUT_HANDLER.PrintError(
              'Unable to configure, with error: {0:s}'.format(repr(exception)))
          gather_answer = cls._OUTPUT_HANDLER.Confirm('Want to try again?')
          if not gather_answer:
            raise

      scaffolder_engine.StoreScaffolderAttribute(
          question.attribute, value, question.TYPE)

  @classmethod
  def GetDefinition(
      cls, definition_string: str) -> definition_interface.ScaffolderDefinition:
    """Returns the definition object as chosen by the user.

    Args:
      definition_string (str): definition name, read from user input.

    Returns:
      definition_interface.ScaffolderDefinition: the chosen definition object.
    """
    definitions = list(
        definition_manager.DefinitionManager.GetDefinitionNames())

    cls._OUTPUT_HANDLER.PrintNewLine()
    if not definition_string:
      cls._OUTPUT_HANDLER.PrintInfo('Available definitions: ')
      definition_string = ''
      while not definition_string:
        try:
          definition_string = cls._GetSelection(definitions, 'Definition')
        except KeyError as e:
          cls._OUTPUT_HANDLER.PrintError('{0!s}'.format(e))

    if definition_string in definitions:
      cls._OUTPUT_HANDLER.PrintOutput('{0:s} chosen.'.format(definition_string))
      def_class = definition_manager.DefinitionManager.GetDefinitionByName(
          definition_string)
      return def_class()

    cls._OUTPUT_HANDLER.PrintError(
        'Definition {0:s} does not exist.'.format(definition_string))
    return cls.GetDefinition('')

  @classmethod
  def GetModuleName(cls) -> str:
    """Returns the module name as chosen by the user."""
    cls._OUTPUT_HANDLER.PrintNewLine()
    cls._OUTPUT_HANDLER.PrintInfo((
        'Name of the module to be generated. This can be something like "'
        'foobar sqlite" or "event analytics".\n\nThis will be used for class '
        'name generation and file name prefixes.'))
    return cls._OUTPUT_HANDLER.PromptInfo('Module Name')

  @classmethod
  def GetProjectPath(
      cls, definition: definition_interface.ScaffolderDefinition) -> str:
    """Returns the path to the project's root folder as chosen by the user.

    Args:
      definition (definition_interface.ScaffolderDefinition): the chosen
          definition. Used to validate the project path.

    Returns:
      str: the path to the project's root folder.

    Raises:
      errors.WrongCliInput: when no valid project path has been provided.
    """
    cls._OUTPUT_HANDLER.PrintNewLine()
    # pylint: disable=assignment-from-no-return
    project_path = cls._OUTPUT_HANDLER.PromptInfo('Path to the project root')
    if definition.ValidatePath(project_path):
      cls._OUTPUT_HANDLER.PrintOutput(
          'Path [{0:s}] set as the project path.'.format(project_path))
      cls._git_helper = git.GitHelper(project_path)
      return project_path

    # pylint: disable=assignment-from-no-return
    check = cls._OUTPUT_HANDLER.Confirm((
        'Path [{0:s}] does not lead to a valid project for {1:s}. '
        'Do you want to try again?').format(project_path, definition.NAME))

    if check:
      return cls.GetProjectPath(definition)

    raise errors.WrongCliInput(
        'Unable to proceed without a valid project path.')

  @classmethod
  def GetScaffolder(
      cls, definition: definition_interface.ScaffolderDefinition
  ) -> scaffolder_interface.Scaffolder:
    """Returns the scaffolder as chosen by the user.

    Args:
      definition (definition_interface.ScaffolderDefinition): the chosen
          definition. Used to determine available scaffolders.

    Returns:
      scaffolder_interface.ScaffolderCli: the chosen scaffolder object.
    """
    scaffolders = {}
    get_scaffolders = scaffolder_manager.ScaffolderManager.GetScaffolders
    for scaffolder_name, scaffolder in get_scaffolders():
      if scaffolder.PROJECT == definition.NAME:
        scaffolders[scaffolder_name] = scaffolder

    cls._OUTPUT_HANDLER.PrintNewLine()
    cls._OUTPUT_HANDLER.PrintInfo(
        'Available scaffolders for {0:s}:'.format(definition.NAME))

    scaffolder = ''
    while not scaffolder:
      try:
        scaffolder = cls._GetSelection(list(scaffolders.keys()), 'Scaffolder')
      except KeyError as e:
        cls._OUTPUT_HANDLER.PrintError('{0!s}'.format(e))
    if scaffolder in scaffolders:
      return scaffolders[scaffolder]()

    cls._OUTPUT_HANDLER.PrintError(
        'Scaffolder: {0:s} does not exist.'.format(scaffolder))
    return cls.GetScaffolder(definition)

  @classmethod
  def Start(cls, definition_value):
    """Start the CLI.

    Args:
      definition_value (str): the definition string chosen by UI.
    """
    cls._OUTPUT_HANDLER.PrintInfo('   == Starting the scaffolder ==')
    cls._OUTPUT_HANDLER.PrintInfo('Gathering all required information.')
    scaffolder_engine = engine.ScaffolderEngine()

    definition = cls.GetDefinition(definition_value)

    project_path = cls.GetProjectPath(definition)
    scaffolder_engine.SetProjectRootPath(project_path)

    module_name = cls.GetModuleName()
    scaffolder_engine.SetModuleName(module_name)
    cls._OUTPUT_HANDLER.PrintInfo(
        'About to create a new feature branch to store newly generated code.')
    try:
      cls.CreateGitFeatureBranch(project_path, scaffolder_engine.module_name)
    except errors.UnableToConfigure as exception:
      cls._OUTPUT_HANDLER.PrintError((
          'Unable to create feature branch, is {0:s} a valid git project path? '
          'The error message was: {1!s}').format(project_path, exception))
      cls._OUTPUT_HANDLER.PrintError('Due to fatal error, not proceeding.')
      return

    scaffolder = cls.GetScaffolder(definition)
    scaffolder_engine.SetScaffolder(scaffolder)
    try:
      cls.GatherScaffolderAnswers(scaffolder, scaffolder_engine)
    except errors.UnableToConfigure as exception:
      # pylint: disable=assignment-from-no-return
      cls._OUTPUT_HANDLER.PrintError(
          'Unable to properly confgure scaffolder, aborting.')
      return

    # pylint: disable=assignment-from-no-return
    ready = cls._OUTPUT_HANDLER.Confirm('Ready to generate files?')
    if ready:
      for file_path in scaffolder_engine.GenerateFiles():
        cls._OUTPUT_HANDLER.PrintOutput(
            'File: {0:s} written to disk.'.format(file_path))
        _, _, file_path_inside_project = file_path.partition(project_path)
        if file_path_inside_project.startswith(os.sep):
          file_path_inside_project = file_path_inside_project[1:]
        cls._git_helper.AddFileToTrack(file_path_inside_project)
