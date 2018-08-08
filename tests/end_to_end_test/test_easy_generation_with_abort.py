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


class EasyGenerationWithAbortTest(unittest.TestCase):
  """Test File for Easy Generation with Abort"""

  def testEasyGenerationWithAbort(self):
    """Test easy file generation without errors and with abort at the end, not
    generating the files.

    1.  plasoscaffolder sqlite
    2.  What's the path to the plaso project?: tmpdir
    3.  What's the name of the plugin?: test
    4.  What's the path to your test file?: test_database/twitter_ios.db
    5.  Do you want to have a output example for your SQL Query? [Y/n]: n
    6.  Please write your SQL script for the plugin: select * from users
    7.  The SQL query was ok.
    8.  Do you want to name the query parse row: Users ? [Y/n]:  Y
    9.  Is the column a time event? updatedAt [Y/n]:  Y
    10. Is the column a time event? createdDate [Y/n]: Y
    11. Enter (additional) timestamp events from the query [column-Name,
        aliasName...] or [abort]: abort
    12. Does the event Users need customizing? [y/N]: N
    13. Do you want to add another Query? [Y/n]: n
    14. Do you want to Generate the files [Y/n]: n
    """
    if platform.system() in ['Linux']:

      with tempfile.TemporaryDirectory() as tmpdir:
        helper = end_to_end_test_helper.EndToEndTestHelper(tmpdir, 'test')
        path_answer = tmpdir

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
        child.sendline(helper.OUTPUT_ANSWER_NO)
        child.expect(helper.OUTPUT_ANSWER_NO)

        child.expect(helper.SQL_QUESTION)
        child.sendline(helper.SQL_ANSWER)
        child.expect(helper.SQL_ANSWER_ESCAPED)
        child.expect(helper.SQL_ANSWER_OK)

        child.expect(helper.NAME_ROW_QUESTION_USERS)
        child.sendline(helper.NAME_ROW_ANSWER_YES)
        child.expect(helper.NAME_ROW_ANSWER_YES)

        child.expect(helper.COLUMN_QUESTION_UPDATED_AT)
        child.sendline(helper.COLUMN_ANSWER_NO)
        child.expect(helper.COLUMN_ANSWER_NO)

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
        child.sendline(helper.GENERATE_ANSWER_NO)
        child.expect('Aborted\!')

        formatter_init = os.path.isfile(helper.formatter_init_path)
        formatter = os.path.isfile(helper.formatter_path)
        formatter_test = os.path.isfile(helper.formatter_test_path)
        parser_init = os.path.isfile(helper.parsers_init_path)
        parser = os.path.isfile(helper.parser_path)
        parser_test = os.path.isfile(helper.parser_test_path)

        self.assertFalse(formatter_init)
        self.assertFalse(formatter)
        self.assertFalse(formatter_test)
        self.assertFalse(parser_init)
        self.assertFalse(parser)
        self.assertFalse(parser_test)
    else:
      raise NotImplementedError("test only implemented for linux platform")

  if __name__ == '__main__':
    unittest.main()
