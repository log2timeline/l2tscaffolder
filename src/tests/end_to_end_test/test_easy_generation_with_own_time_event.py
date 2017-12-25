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


class EasyGenerationWithOwnTimeEventTest(unittest.TestCase):
  """Test file for generation with time event."""

  def testEasyGenerationWithOwnTimeEvent(self):
    """Test easy file generation without errors

    1.  plasoscaffolder sqlite
    2.  What's the path to the plaso project?: tmpdir
    3.  What's the name of the plugin?: test
    4.  What's the path to your test file?: test_database/twitter_ios.db
    5.  Do you want to have a output example for your SQL Query? [Y/n]: n
    6.  Please write your SQL script for the plugin: select * from users
    7.  The SQL query was ok.
    8.  Do you want to name the query parse row: Users ? [Y/n]: Y
    9.  Is the column a time event? updatedAt [Y/n]:  n
    10. Is the column a time event? createdDate [Y/n]: Y
    11. Enter (additional) timestamp events from the query [column-Name,
        aliasName...] or [abort]: id that this
    12. Timestamps are not in valid format. Reenter them correctly [name,
        name...]: id, that, this
    13. Timestamps are not in valid format. Reenter them correctly [name,
        name...]:id,that,this
    14. Added: createdDate,id
        Failed: that,this
    15. Do you want to add more timestamps? [y/N]: y
    16. Enter (additional) timestamp events from the query [column-Name,
        aliasName...] or [abort]: name,that
    17. Added: createdDate,id,name
    18. Failed: that,this
    19. Do you want to add more timestamps? [y/N]: n
    20. Does the event Users need customizing? [y/N]: N
    21. Do you want to add another Query? [Y/n]: n
    22. Do you want to Generate the files [Y/n]: Y

    """
    if platform.system() in ['Linux']:
      with tempfile.TemporaryDirectory() as tmpdir:
        helper = end_to_end_test_helper.EndToEndTestHelper(tmpdir, 'test')

        path_answer = tmpdir
        expected_path = os.path.join(helper.DIR_PATH,
                                     'ExpectedEasyGenerationOwnTimestampFiles')

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
        child.sendline('id that this')
        child.expect('id that this')

        child.expect(helper.ADDITIONAL_TIMESTAMP_INVALID)
        child.sendline('id, that, this')
        child.expect('id\, that\, this')

        child.expect(helper.ADDITIONAL_TIMESTAMP_INVALID)
        child.sendline('id,that,this')
        child.expect('id\,that\,this')
        child.expect('Added\: createdDate\,id')
        child.expect('Failed\: that\,this')

        child.expect(helper.MORE_TIMESTAMPS_QUESTION)
        child.sendline(helper.MORE_TIMESTAMPS_ANSWER_YES)

        child.expect(helper.ADDITIONAL_TIMESTAMP)
        child.sendline('name,that')
        child.expect('name\,that')
        child.expect('Added\: createdDate\,id\,name')
        child.expect('Failed\: that\,this')

        child.expect(helper.MORE_TIMESTAMPS_QUESTION)
        child.sendline(helper.MORE_TIMESTAMPS_ANSWER_NO)

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
