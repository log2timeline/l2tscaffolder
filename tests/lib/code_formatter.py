# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the code formatter."""
import unittest

from l2tscaffolder.lib import code_formatter
from tests.test_helper import path_helper


class CodeFormatterTest(unittest.TestCase):
  """Test case for the code formatter functions. """

  def testCodeFormatter(self):
    """Tests the code formatter.."""
    yapf_path = path_helper.YapfStyleFilePath()
    formatter = code_formatter.CodeFormatter(yapf_path)

    faulty_code_string = (
        'class Foobar(object):\n'
        '\n'
        '  def SetStuff(self):\n'
        '  return None\n')

    with self.assertRaises(IndentationError):
      _ = formatter.Format(faulty_code_string)

    code_string = (
        'class Foobar(object):\n  """This is a class like no other '
        'class."""\n\n  def Foobar(self, s):\n    """Foobar is the foobar."""\n'
        '\n    thisIsAReallyLongVariable = os.path.join('
        '"foobar", "another", "lets see", "yet", "formal", "informal", "direct"'
        ', "indirect")\n')
    formatted_code, code_changed = formatter.Format(code_string)

    correct_code = (
        'class Foobar(object):\n'
        '  """This is a class like no other class."""\n'
        '\n'
        '  def Foobar(self, s):\n'
        '    """Foobar is the foobar."""\n'
        '\n'
        '    thisIsAReallyLongVariable = os.path.join(\n'
        '        "foobar", "another", "lets see", "yet", "formal", '
        '"informal", "direct",\n'
        '        "indirect")\n')

    self.assertTrue(code_changed)
    self.assertEqual(formatted_code, correct_code)


if __name__ == '__main__':
  unittest.main()
