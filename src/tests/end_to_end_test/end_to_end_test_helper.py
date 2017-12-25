# -*- coding: utf-8 -*-
# disable backslash in string because special characters need to be escaped
# pylint: disable=anomalous-backslash-in-string
"""class for end to end test helper"""
import os

from tests.test_helper import path_helper


class EndToEndTestHelper(object):
  """Class defining Variables to be used multiple times in tests"""
  DIR_PATH = os.path.dirname(os.path.realpath(__file__))
  DATABASE_PATH = path_helper.TestDatabasePath()
  MAIN_PATH = os.path.join(
      os.path.dirname(os.path.dirname(DIR_PATH)), 'plasoscaffolder',
      'frontend', 'main.py')
  PATH_QUESTION = 'What\'s the path to the plaso project\?\:'
  PATH_WRONG_QUESTION = 'Folder does not exists\. Enter correct one'
  NAME_QUESTION = 'What\'s the name of the plugin\?\:'
  NAME_QUESTION_NOT_VALID = ('Plugin is not in a valid format\. Choose new '
                             'Name \[plugin\_name\_\.\.\.\]')
  NAME_QUESTION_EXISTS = 'Plugin exists\. Choose new Name'

  NAME_ANSWER = 'test'
  TESTFILE_QUESTION = 'What\'s the path to your test file\?\:'
  TESTFILE_QUESTION_NOT_FOUND = "File does not exists\. Choose another\."
  TESTFILE_QUESTION_INVALID = 'Unable to open the database file\. Choose ' \
                              'another\.'
  TESTFILE_ANSWER = os.path.join(DATABASE_PATH, 'twitter_ios.db')
  TESTFILE_ANSWER_ERROR = os.path.join(DATABASE_PATH, 'twitter_ios_error.db')
  TESTFILE_ANSWER_NOT_FOUND = os.path.join(DATABASE_PATH, 'does_not_exist')

  OUTPUT_QUESTION = ('Do you want to have a output example for your '
                     'SQL Query\? \[Y\/n\]\:')
  OUTPUT_ANSWER_NO = 'n'
  OUTPUT_ANSWER_YES = 'y'
  OUTPUT_ADD_QUESTION = 'Do you want to add this query\? \[Y\/n\]\:'
  OUTPUT_ADD_ANSWER_NO = 'n'
  OUTPUT_ADD_ANSWER_YES = 'y'
  OUTPUT_EXAMPLE_FIRST_ROW = 'Your query output could look like this\.'
  OUTPUT_USERS_ID_NAME_EXAMPLE_HEADER = '\[\'id\'\, \'name\'\, ' \
                                        '\'createdDate\'\]'
  OUTPUT_USERS_ID_EXAMPLE_FIRST_ROW = '\(5402612\, \'BBC Breaking News\'\, ' \
                                      '1177252957\.0\)'
  OUTPUT_USERS_ID_EXAMPLE_SECOND_ROW = '\(13334762\, \'GitHub\'\, ' \
                                       '1202704910\.0\)'
  OUTPUT_USERS_ID_EXAMPLE_THIRD_ROW = '\(14388264\, \'Tom Pohl\'\, ' \
                                      '1208195714\.0\)'

  SQL_QUESTION = 'Please write your SQL script for the plugin\:'
  SQL_QUESTION_WITH_ABORT = ('Please write your SQL script for the plugin '
                             '\[\'abort\' to continue\]\:')
  SQL_ANSWER = 'select * from users'
  SQL_ANSWER_ESCAPED = 'select \* from users'
  SQL_ANSWER_2 = 'select * from statuses'
  SQL_ANSWER_ESCAPED_2 = 'select \* from statuses'
  SQL_ANSWER_ID_NAME = 'select id, name, createdDate from users'
  SQL_ANSWER_ESCAPED_ID_NAME = 'select id\, name\, createdDate from users'
  SQL_ANSWER_OK = 'The SQL query was ok.'
  NAME_ROW_QUESTION_USERS = ('Do you want to name the query parse row\: '
                             'Users \? \[Y\/n\]\:')
  NAME_ROW_QUESTION_STATUSES = ('Do you want to name the query parse row\: '
                                'Statuses \? \[Y\/n\]\:')
  NAME_ROW_QUESTION_USERSSTATUSES = ('Do you want to name the query parse row\:'
                                     ' Usersstatuses \? \[Y\/n\]\:')
  NAME_ROW_QUESTION_INVALID = ('Row name is not in a valid format\. '
                               'Choose new Name \[RowName\.\.\.\]')
  NAME_ROW_QUESTION_QUERY = 'What row does the SQL Query parse\?\:'
  NAME_ROW_ANSWER_YES = 'Y'
  NAME_ROW_ANSWER_NO = 'N'
  COLUMN_ANSWER_YES = 'Y'
  COLUMN_ANSWER_NO = 'N'
  COLUMN_QUESTION_CREATED_DATE = ('Is the column a time event\? createdDate \['
                                  'Y\/n\]\:')
  COLUMN_QUESTION_UPDATED_AT = ('Is the column a time event\? updatedAt \['
                                'Y\/n\]\:')
  COLUMN_QUESTION_DATE = ('Is the column a time event\? date \['
                          'Y\/n\]\:')
  COLUMN_QUESTION_PROFILE_TIMELINE = ('Is the column a time event\? '
                                      'includeInProfileTimeline \['
                                      'Y\/n\]\:')
  ADDITIONAL_TIMESTAMP = ('Enter \(additional\) timestamp events from '
                          'the query \[columnName,aliasName...\] or \['
                          'abort\]\:')
  ADDITIONAL_TIMESTAMP_INVALID = ('Timestamps are not in valid format\. '
                                  'Reenter them correctly \[name\,name\.\.\.\]')
  MORE_TIMESTAMPS_QUESTION = 'Do you want to add more timestamps\? \[y\/N\]\:'
  MORE_TIMESTAMPS_ANSWER_NO = 'N'
  MORE_TIMESTAMPS_ANSWER_YES = 'Y'
  ADDITIONAL_TIMESTAMP_ABORT = 'abort'
  CUSTOM_QUESTION_USERS = ('Does the event Users need customizing\? \['
                           'y\/N\]\:')
  CUSTOM_QUESTION_USERSSTATUSES = ('Does the event Usersstatuses need '
                                   'customizing\? \[y\/N\]\:')
  CUSTOM_QUESTION_STATUSES = ('Does the event Statuses need customizing\? \['
                              'y\/N\]\:')
  CUSTOM_QUESTION_THEUSER = ('Does the event TheUser need customizing\? \['
                             'y\/N\]\:')
  CUSTOM_ANSWER_NO = 'N'
  CUSTOM_ANSWER_YES = 'Y'
  CUSTOM_ADD_QUESTION = ('Enter columns that are customizable '
                         '\[columnName\,aliasName\.\.\.\] or \[abort\]\:')
  CUSTOM_ADD_INVALID = ('Column names are not in valid format\. '
                        'Reenter them correctly \[name\,name\.\.\.\]')
  CUSTOM_ADD_MORE_QUESTION = ('Do you want to add more columns '
                              'that are customizable\? \[y\/N\]\:')
  CUSTOM_ADD_MORE_ANSWER_NO = 'N'
  CUSTOM_ADD_MORE_ANSWER_YES = 'Y'
  ADD_QUESTION = 'Do you want to add another Query\? \[Y\/n\]\:'
  ADD_ANSWER_NO = 'n'
  ADD_ANSWER_YES = 'Y'
  GENERATE_QUESTION = 'Do you want to Generate the files\? \[Y\/n\]\:'
  GENERATE_ANSWER_YES = 'Y'
  GENERATE_ANSWER_NO = 'N'

  def __init__(self, plaso_dir_path: str, name: str):
    """Initializes the test helper

    Args:
      plaso_dir_path (str): the path of the directory of plaso
      name (str): the name of the plugin.
    """
    self.formatter_path = os.path.join(
        plaso_dir_path, 'plaso/formatters/{0}.py'.format(name))
    self.parser_path = os.path.join(
        plaso_dir_path, 'plaso/parsers/sqlite_plugins/{0}.py'.format(name))
    self.formatter_test_path = os.path.join(
        plaso_dir_path, 'tests/formatters/{0}.py'.format(name))
    self.parser_test_path = os.path.join(
        plaso_dir_path, 'tests/parsers/sqlite_plugins/{0}.py'.format(name))
    self.test_data_path = os.path.join(
        plaso_dir_path, 'test_data/{0}.db'.format(name))
    self.parsers_init_path = os.path.join(
        plaso_dir_path, 'plaso/parsers/sqlite_plugins/__init__.py')
    self.formatter_init_path = os.path.join(
        plaso_dir_path, 'plaso/formatters/__init__.py')

  def ReadFromFile(self, path: str):
    """read from file helper"""
    with open(path, 'r') as f:
      return f.read()
