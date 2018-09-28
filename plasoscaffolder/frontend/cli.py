# !/usr/bin/python
# -*- coding: utf-8 -*-
"""The scaffolder CLI frontend."""
import collections
import re

from typing import Dict
from typing import List
from typing import Type

import click

from plasoscaffolder.frontend import output_handler
from plasoscaffolder.helpers import git
from plasoscaffolder.lib import engine
from plasoscaffolder.lib import errors

from plasoscaffolder.definitions import interface as definition_interface
from plasoscaffolder.definitions import manager as definition_manager
from plasoscaffolder.scaffolders import interface as scaffolder_interface
from plasoscaffolder.scaffolders import manager as scaffolder_manager


class ScaffolderCli:
  """A CLI implementation for the scaffolder project.

  Attributes:
    OUTPUT_HANDLER (output_handler.OutputHandlerClick: output handler
        that is used to request and read input from end user.
  """

  OUTPUT_HANDLER = output_handler.OutputHandlerClick()

  @classmethod
  def _AskDictQuestion(
      cls, question: scaffolder_interface.BaseQuestion) -> Dict[str, Type]:
    """Ask the user a question and return a dict answer back.

    Args:
      question (scaffolder_interface.BaseQuestion): the question to ask.

    Returns:
      dict: the answer as supplied by the user.
    """
    return_dict = {}

    more_entries = True
    entry_index = 1
    while more_entries:
      key = cls.OUTPUT_HANDLER.PromptInfo(
          '{0:s} [#{1:d}]'.format(question.key_prompt, entry_index))
      if key in return_dict:
        cls.OUTPUT_HANDLER.PrintError(
            'Key value ({0:s}) already entered.'.format(key))
        continue

      value = cls.OUTPUT_HANDLER.PromptInfo(
          '{0:s} [#{1:d}]'.format(question.value_prompt, entry_index))

      return_dict[key] = value
      more_entries = cls.OUTPUT_HANDLER.Confirm('More entries?', abort=False)
      entry_index += 1

    question.ValidateAnswer(return_dict)
    return return_dict

  @classmethod
  def _AskListQuestion(
      cls, question: scaffolder_interface.BaseQuestion) -> List[object]:
    """Ask the user a question and return a list back.

    Args:
      question (scaffolder_interface.BaseQuestion): the question to ask.

    Returns:
      list: the answer as supplied by the user.
    """
    return_list = []

    more_entries = True
    entry_index = 1
    while more_entries:
      value = cls.OUTPUT_HANDLER.PromptInfo(
          'Value to add [#{0:d}]'.format(entry_index))
      if not value:
        cls.OUTPUT_HANDLER.PrintError('Empty value, not adding.')
      else:
        return_list.append(value)

      more_entries = cls.OUTPUT_HANDLER.Confirm('Add more values?', abort=False)
      entry_index += 1

    question.ValidateAnswer(return_list)
    return return_list

  @classmethod
  def _AskQuestion(cls, question: scaffolder_interface.BaseQuestion) -> Type:
    """Ask the user a question and return an answer back.

    Args:
      question (scaffolder_interface.BaseQuestion): the question to ask.

    Returns:
      object: an object, whos type is defined in question.type.

    Raises:
      errors.WrongCliInput: when an unsupported question type is
          encountered.
    """
    cls.OUTPUT_HANDLER.PrintNewLine()
    cls.OUTPUT_HANDLER.PrintInfo(question.prompt)

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
      cls, question: scaffolder_interface.BaseQuestion) -> str:
    """Ask the user a question and return a string answer back.

    Args:
      question (scaffolder_interface.BaseQuestion): the question to ask.

    Returns:
      str: the answer as supplied by the user.
    """
    value = cls.OUTPUT_HANDLER.PromptInfo('Value')
    question.ValidateAnswer(value)
    return value

  @classmethod
  def _GetSelection(cls, items: list, item_text: str) -> str:
    """Present a list of items to user and return back the chosen one.

    Args:
      items (list): the list of items to present to the user.
      item_text (str): heading used in presentation to the user.

    Returns:
      str: the chosen item from the list.
    """
    for item_count, item in enumerate(items):
      cls.OUTPUT_HANDLER.PrintInfo(
          '  [{0:d}] {1:s}'.format(item_count + 1, item))

    result = cls.OUTPUT_HANDLER.PromptInfo('{0:s} choice'.format(item_text))
    try:
      result_int = int(result, 10)

      if result_int <= len(items):
        return items[result_int - 1]
    except ValueError:
      pass

    return result

  @classmethod
  def CreateGitFeatureBranch(cls, project_path: str, module_name: str):
    """Create a feature branch inside the git project.

    Creates a feature branch inside the git project path
    to store all the generated files in.

    Args:
      project_path (str): path to the git project folder.
      module_name (str): name of the output module.
    """
    git_helper = git.GitHelper(project_path)
    active_branch = git_helper.GetActiveBranch()

    branch_name = re.sub('(?<!^)(?=[A-Z])', '_', module_name).lower()
    if active_branch == branch_name:
      cls.OUTPUT_HANDLER.PrintOutput((
          'Feature branch [{0:s}] already exists and is the '
          'active branch').format(branch_name))
      return

    git_helper.CreateFeatureBranch(branch_name)
    cls.OUTPUT_HANDLER.PrintOutput(
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
          cls.OUTPUT_HANDLER.PrintError(
              'Unable to configure, with error: {0:s}'.format(repr(exception)))
          gather_answer = cls.OUTPUT_HANDLER.Confirm('Want to try again?')
          if not gather_answer:
            raise

      scaffolder_engine.StoreScaffolderAttribute(
          question.attribute, value, question.TYPE)

  @classmethod
  def GetDefinition(
      cls, definition_string: str) -> definition_interface.ScaffolderDefinition:
    """Return the definition object as chosen by the user.

    Args:
      definition_string (str): definition name, read from user input.

    Returns:
      definition_interface.ScaffolderDefinition: the chosen definition object.
    """
    definitions = list(
        definition_manager.DefinitionManager.GetDefinitionNames())

    cls.OUTPUT_HANDLER.PrintNewLine()
    if not definition_string:
      cls.OUTPUT_HANDLER.PrintInfo('Available definitions: ')
      definition_string = cls._GetSelection(definitions, 'Definition')

    if definition_string in definitions:
      cls.OUTPUT_HANDLER.PrintOutput('{0:s} chosen.'.format(definition_string))
      def_class = definition_manager.DefinitionManager.GetDefinitionByName(
          definition_string)
      return def_class()

    cls.OUTPUT_HANDLER.PrintError(
        'Definition {0:s} does not exist.'.format(definition_string))
    return cls.GetDefinition('')

  @classmethod
  def GetModuleName(cls) -> str:
    """Return the module name as chosen by the user."""
    cls.OUTPUT_HANDLER.PrintNewLine()
    cls.OUTPUT_HANDLER.PrintInfo((
        'Name of the module to be generated. This can be something like "'
        'foobar sqlite" or "event analytics".\n\nThis will be used for class '
        'name generation and file name prefixes.'))
    return cls.OUTPUT_HANDLER.PromptInfo('Module Name')

  @classmethod
  def GetProjectPath(
      cls, definition: definition_interface.ScaffolderDefinition) -> str:
    """Return the path to the project as chosen by the user.

    Args:
      definition (definition_interface.ScaffolderDefinition): the chosen
          definition. Used to validate the project path.

    Returns:
      str: the path to the project file.

    Raises:
      errors.WrongCliInput: when no valid project path has been provided.
    """
    cls.OUTPUT_HANDLER.PrintNewLine()
    project_path = cls.OUTPUT_HANDLER.PromptInfo('Path to the project root')
    if definition.ValidatePath(project_path):
      cls.OUTPUT_HANDLER.PrintOutput(
          'Path [{0:s}] set as the project path.'.format(project_path))
      return project_path

    check = cls.OUTPUT_HANDLER.Confirm((
        'Path [{0:s}] does not lead to a valid project for {1:s}. '
        'Do you want to try again?').format(project_path, definition.NAME))

    if check:
      return cls.GetProjectPath(definition)

    raise errors.WrongCliInput(
        u'Unable to proceed without a valid project path.')

  @classmethod
  def GetScaffolder(
      cls, definition: definition_interface.ScaffolderDefinition
  ) -> scaffolder_interface.Scaffolder:
    """Return the scaffolder as chosen by the user.

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

    cls.OUTPUT_HANDLER.PrintNewLine()
    cls.OUTPUT_HANDLER.PrintInfo(
        'Available scaffolders for {0:s}:'.format(definition.NAME))

    scaffolder = cls._GetSelection(list(scaffolders.keys()), 'Scaffolder')
    if scaffolder in scaffolders:
      return scaffolders[scaffolder]()

    cls.OUTPUT_HANDLER.PrintError(
        'Scaffolder: {0:s} does not exist.'.format(scaffolder))
    return cls.GetScaffolder(definition)

  @classmethod
  def Start(
      cls, unused_ctx: click.core.Context, unused_param: click.core.Option,
      value: str):
    """Start the CLI.

    Args:
      unused_ctx (click.core.Context): the click context (automatically given
        via callback)
      unused_param (click.core.Option): the click command (automatically
        given via callback)
      value (str): the definition string (automatically given via callback)
    """
    cls.OUTPUT_HANDLER.PrintInfo('   == Starting the scaffolder ==')
    cls.OUTPUT_HANDLER.PrintInfo('Gathering all required information.')
    scaffolder_engine = engine.ScaffolderEngine()

    definition = cls.GetDefinition(value)

    project_path = cls.GetProjectPath(definition)
    scaffolder_engine.SetProjectRootPath(project_path)

    module_name = cls.GetModuleName()
    scaffolder_engine.SetModuleName(module_name)
    try:
      cls.CreateGitFeatureBranch(project_path, scaffolder_engine.module_name)
    except errors.UnableToConfigure as exception:
      cls.OUTPUT_HANDLER.PrintError((
          'Unable to create feature branch, is this a valid git project path? '
          'The error message was: {0:s}').format(repr(exception)))
      cls.OUTPUT_HANDLER.PrintError('Due to fatal error, not proceeding.')
      return

    scaffolder = cls.GetScaffolder(definition)
    scaffolder_engine.SetScaffolder(scaffolder)
    try:
      cls.GatherScaffolderAnswers(scaffolder, scaffolder_engine)
    except errors.UnableToConfigure as exception:
      cls.OUTPUT_HANDLER.PrintError(
          'Unabl to properly confgure scaffolder, aborting.')
      return

    ready = cls.OUTPUT_HANDLER.Confirm('Ready to generate files?')
    if ready:
      for file_path in scaffolder_engine.GenerateFiles():
        cls.OUTPUT_HANDLER.PrintOutput(
            'File: {0:s} written to disk.'.format(file_path))
