# !/usr/bin/python
# -*- coding: utf-8 -*-
# disable backslash in string because special characters need to be escaped
# pylint: disable=anomalous-backslash-in-string
"""Test Class for end to end Tests.
These Tests can only be run on Linux because it makes use of pexpect."""

import os
import platform
import tempfile
import unittest

import pexpect
from tests.end_to_end_test import end_to_end_test_helper


class SelectWithSpecialCharactersTest(unittest.TestCase):
  """Test file for select with special characters."""

  def testSelectWithSpecialCharacters(self):
    """Test different queries with special characters

    1.  plasoscaffolder sqlite
    2.  What's the path to the plaso project?: tmpdir
    3.  What's the name of the plugin?: test
    4.  What's the path to your test file?: test_database/twitter_ios.db
    5.  Do you want to have a output example for your SQL Query? [Y/n]: n
    6.  Please write your SQL script for the plugin: select users.id as
        “userid” from users join statuses
    7.  Info: Don’t use any characters beside a-z A-Z . ; , *
    8.  Please write your SQL script for the plugin: select hex(id) from users
    9.  Warning: Don’t use any characters beside a-z A-Z . ; , *
    10. Please write your SQL script for the plugin: select [AS].[ID] AS [the
        alias], [AS].name AS “the name” , S.id from users as [AS] join statuses
        as “S”
    11. Warning: Don’t use any characters beside a-z A-Z . ; , *
    12. Please write your SQL script for the plugin: select id as the-id from
        user
    13. Warning: Don’t use any characters beside a-z A-Z . ; , *
    14. Please write your SQL script for the plugin: select somealias.id from
        users as somealias
    15. Warning: Don’t use any alias for a table name
    16. Please write your SQL script for the plugin: select * from users
    17. The SQL query was ok.
    18. Do you want to name the query parse row: Users ? [Y/n]:  Y
    19. Is the column a time event? updatedAt [Y/n]:  Y
    20. Is the column a time event? createdDate [Y/n]: Y
    21. Enter (additional) timestamp events from the query [column-Name,
        aliasName...] or [abort]: abort
    22. Does the event Users need customizing? [y/N]: N
    23. Do you want to add another Query? [Y/n]: n
    24. Do you want to Generate the files [Y/n]: Y

    """
    if platform.system() in ['Linux']:

      with tempfile.TemporaryDirectory() as tmpdir:
        helper = end_to_end_test_helper.EndToEndTestHelper(tmpdir, 'test')

        path_answer = tmpdir
        expected_path = os.path.join(helper.DIR_PATH,
                                     'ExpectedEasyGenerationFiles')

        command = 'python {0} sqlite'.format(helper.MAIN_PATH)
        child = pexpect.spawn(command)

        child.expect(helper.PATH_QUESTION)
        child.sendline(path_answer)
        child.expect(path_answer)

        child.expect(helper.NAME_QUESTION)
        child.sendline(helper.NAME_ANSWER)
        child.expect(helper.NAME_ANSWER)

        child.expect(helper.TESTFILE_QUESTION)
        child.sendline(helper.TESTFILE_ANSWER)
        child.expect(helper.TESTFILE_ANSWER)

        child.expect(helper.OUTPUT_QUESTION)
        child.sendline(helper.COLUMN_ANSWER_NO)
        child.expect(helper.COLUMN_ANSWER_NO)

        child.expect(helper.SQL_QUESTION)
        child.sendline('select users.id as "userid" from users join statuses')
        child.expect('select users\.id as \"userid\" from users join statuses')
        child.expect('Warning\: Don\'t use any characters beside '
                     'a\-z A\-Z 0\-9 \. \; \, \* \= \_')

        child.expect(helper.SQL_QUESTION)
        child.sendline('select hex(id) from users')
        child.expect('select hex\(id\) from users')
        child.expect('Warning\: Don\'t use any characters beside '
                     'a\-z A\-Z 0\-9 \. \; \, \* \= \_')

        child.expect(helper.SQL_QUESTION)
        child.sendline('select [AS].[ID] AS [the alias], '
                       '[AS].name AS "the name" , S.id from users as [AS] '
                       'join statuses as "S"')
        child.expect('select \[AS\]\.\[ID\] AS \[the alias\]\, '
                     '\[AS\]\.name AS \"the name\" \, S\.id '
                     'from users as \[AS\] join statuses as \"S\"')
        child.expect('Warning\: Don\'t use any characters beside '
                     'a\-z A\-Z 0\-9 \. \; \, \* \= \_')

        child.expect(helper.SQL_QUESTION)
        child.sendline('select id as the-id from users')
        child.expect('select id as the\-id from users')
        child.expect('Warning\: Don\'t use any characters beside '
                     'a\-z A\-Z 0\-9 \. \; \, \* \= \_')

        child.expect(helper.SQL_QUESTION)
        child.sendline('select somealias.id from users as somealias')
        child.expect('select somealias\.id from users as somealias')
        child.expect('Warning\: Don\'t use any alias for a table name')

        child.expect(helper.SQL_QUESTION)
        child.sendline(helper.SQL_ANSWER)
        child.expect(helper.SQL_ANSWER_ESCAPED)
        child.expect(helper.SQL_ANSWER_OK)

        child.expect(helper.NAME_ROW_QUESTION_USERS)
        child.sendline(helper.NAME_ROW_ANSWER_YES)
        child.expect(helper.NAME_ROW_ANSWER_YES)

        child.expect(helper.COLUMN_QUESTION_UPDATED_AT)
        child.sendline(helper.COLUMN_ANSWER_YES)
        child.expect(helper.COLUMN_ANSWER_YES)

        child.expect(helper.COLUMN_QUESTION_CREATED_DATE)
        child.sendline(helper.COLUMN_ANSWER_YES)
        child.expect(helper.COLUMN_ANSWER_YES)

        child.expect(helper.ADDITIONAL_TIMESTAMP)
        child.sendline(helper.ADDITIONAL_TIMESTAMP_ABORT)
        child.expect(helper.ADDITIONAL_TIMESTAMP_ABORT)

        child.expect(helper.CUSTOM_QUESTION_USERS)
        child.sendline(helper.CUSTOM_ANSWER_NO)
        child.expect(helper.CUSTOM_ANSWER_NO)

        child.expect(helper.ADD_QUESTION)
        child.sendline(helper.ADD_ANSWER_NO)
        child.expect(helper.ADD_ANSWER_NO)

        child.expect(helper.GENERATE_QUESTION)
        child.sendline(helper.GENERATE_ANSWER_YES)

        child.expect('create.*{0}'.format(helper.formatter_path))
        child.expect('create.*{0}'.format(helper.parser_path))
        child.expect('create.*{0}'.format(helper.formatter_test_path))
        child.expect('create.*{0}'.format(helper.parser_test_path))
        child.expect('copy.*{0}'.format(helper.test_data_path))
        child.expect('create.*{0}'.format(helper.parsers_init_path))
        child.expect('create.*{0}'.format(helper.formatter_init_path))

        formatter_init = helper.ReadFromFile(helper.formatter_init_path)
        formatter = helper.ReadFromFile(helper.formatter_path)
        formatter_test = helper.ReadFromFile(helper.formatter_test_path)
        parser_init = helper.ReadFromFile(helper.parsers_init_path)
        parser = helper.ReadFromFile(helper.parser_path)
        parser_test = helper.ReadFromFile(helper.parser_test_path)

        expected_formatter_init = helper.ReadFromFile(os.path.join(
            expected_path, 'formatters_init.py'))
        expected_formatter = helper.ReadFromFile(
            os.path.join(expected_path, 'formatters.py'))
        expected_formatter_test = helper.ReadFromFile(os.path.join(
            expected_path, 'formatters_test.py'))
        expected_parser_init = helper.ReadFromFile(
            os.path.join(expected_path, 'parsers_init.py'))
        expected_parser = helper.ReadFromFile(
            os.path.join(expected_path, 'parsers.py'))
        expected_parser_test = helper.ReadFromFile(
            os.path.join(expected_path, 'parsers_test.py'))

        self.assertEqual(formatter_init, expected_formatter_init)
        self.assertEqual(formatter, expected_formatter)
        self.assertEqual(formatter_test, expected_formatter_test)
        self.assertEqual(parser_init, expected_parser_init)
        self.assertEqual(parser, expected_parser)
        self.assertEqual(parser_test, expected_parser_test)
    else:
      raise NotImplementedError("test only implemented for linux platform")

    if __name__ == '__main__':
      unittest.main()
