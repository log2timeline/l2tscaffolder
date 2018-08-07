# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Test Class for end to end Tests.
These Tests can only be run on Linux because it makes use of pexpect."""

import os
import platform
import tempfile
import unittest

import pexpect
from tests.end_to_end_test import end_to_end_test_helper


class EasyGenerationWithOutputTest(unittest.TestCase):
  """Test File for an Easy Generation Test With Output"""

  def testEasyGenerationWithOutputExample(self):
    """Test easy file generation without errors and with an output example

    1.  plasoscaffolder sqlite
    2.  What's the path to the plaso project?: [pfad]
    3.  What's the name of the plugin?: test
    4.  What's the path to your test file?: [pfad_file]
    5.  Do you want to have a output example for your SQL Query? [Y/n]: Y
    6.  Please write your SQL script for the plugin: select id, name,
        createdDate from users
    7.  Your query output could look like this.
        ['id', 'name']
        (5402612, 'BBC Breaking News')
        (13334762, 'GitHub')
        (14388264, 'Tom Pohl')
    8.  Do you want to add this query? [Y/n]: Y
    9.  Do you want to name the query parse row: Users ? [Y/n]:  Y
    10. Is the column a time event? createdDate [Y/n]: Y
    11. Enter (additional) timestamp events from the query [column-Name,
        aliasName...] or [abort]: abort
    12. Does the event Users need customizing? [y/N]: N
    13. Do you want to add another Query? [Y/n]: n

    """
    if platform.system() in ['Linux']:

      with tempfile.TemporaryDirectory() as tmpdir:
        helper = end_to_end_test_helper.EndToEndTestHelper(tmpdir, 'test')

        path_answer = tmpdir
        expected_path = os.path.join(helper.DIR_PATH,
                                     'ExpectedEasyGenerationWithOutputFiles')

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
        child.sendline(helper.OUTPUT_ANSWER_YES)
        child.expect(helper.OUTPUT_ANSWER_YES)

        child.expect(helper.SQL_QUESTION)
        child.sendline(helper.SQL_ANSWER_ID_NAME)
        child.expect(helper.SQL_ANSWER_ESCAPED_ID_NAME)
        child.expect(helper.OUTPUT_EXAMPLE_FIRST_ROW)
        child.expect(helper.OUTPUT_USERS_ID_NAME_EXAMPLE_HEADER)
        child.expect(helper.OUTPUT_USERS_ID_EXAMPLE_FIRST_ROW)
        child.expect(helper.OUTPUT_USERS_ID_EXAMPLE_SECOND_ROW)
        child.expect(helper.OUTPUT_USERS_ID_EXAMPLE_THIRD_ROW)

        child.expect(helper.OUTPUT_ADD_QUESTION)
        child.sendline(helper.OUTPUT_ADD_ANSWER_YES)
        child.expect(helper.OUTPUT_ADD_ANSWER_YES)

        child.expect(helper.NAME_ROW_QUESTION_USERS)
        child.sendline(helper.NAME_ROW_ANSWER_YES)
        child.expect(helper.NAME_ROW_ANSWER_YES)

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
