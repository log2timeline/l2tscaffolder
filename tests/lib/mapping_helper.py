# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the mapping helper."""
import unittest

from l2tscaffolder.lib import mapping_helper
from tests.test_helper import path_helper

# pylint: disable=protected-access
class MappingHelperTest(unittest.TestCase):
  """Tests for the mapping helper."""

  def setUp(self):
    self.template_path = path_helper.TestTemplatePath()
    yapf_path = path_helper.YapfStyleFilePath()
    self.plugin_name = 'the_one_and_only'
    self.file = 'test_template.jinja2'
    self.helper = mapping_helper.MappingHelper(
        formatter_path=yapf_path, template_path=self.template_path)

  def testRender(self):
    """Tests the render method."""
    context = {'plugin_name': self.plugin_name}
    actual = self.helper.RenderTemplate(self.file, context)
    expected = '# -*- coding: utf-8 -*-\n"""{0}"""\n'.format(
        self.plugin_name)
    self.assertEqual(expected, actual)

  def testGenerateClassName(self):
    """Tests the generation of the class name."""
    name = 'this_is_a_test'
    expected = 'ThisIsATest'
    actual = self.helper.GenerateClassName(name)
    self.assertEqual(expected, actual)

  def testRemoveEscapeErrorWithSpacesLikeInTemplate(self):
    """Tests the removing of an escape error"""
    string_with_error = 'u\'the first line\\\'\n        u\'\\the second line'
    string_without_error = 'u\'the first line\'\n        u\'\\\\the second line'
    actual = self.helper._RemoveEscapeError(string_with_error)
    self.assertEqual(string_without_error, actual)

  def testRemoveEscapeErrorWithNoEscape(self):
    """Tests the removing of an escape error"""
    string_without_error = 'u\'the first line\\\\\'\n        u\'the second line'
    actual = self.helper._RemoveEscapeError(string_without_error)
    self.assertEqual(string_without_error, actual)

  def testRemovewhitespaceAtEndOfLineForTwowhitespace(self):
    """Tests the removing of whitespace at the end of a line."""
    string_with_blank = 'somestuff  \n'
    string_without_blank = 'somestuff\n'
    actual = self.helper._RemoveWhitespaceAtEndOfLine(string_with_blank)
    self.assertEqual(string_without_blank, actual)

  def testRemoveWhitespaceAtEndOfLineForFourWhitespace(self):
    """Tests the removing of whitespace at the end of a line."""
    string_with_blank = '    \n'
    string_without_blank = '\n'
    actual = self.helper._RemoveWhitespaceAtEndOfLine(string_with_blank)
    self.assertEqual(string_without_blank, actual)

  def testRemoveWhitespaceAtEndOfLineFor12Whitespace(self):
    """Tests the removing of whitespace at the end of a line"""
    string_with_blank = 'somestuff            \n'
    string_without_blank = 'somestuff\n'
    actual = self.helper._RemoveWhitespaceAtEndOfLine(string_with_blank)
    self.assertEqual(string_without_blank, actual)

  def testRemoveYapfCommentOnlyTheEnable(self):
    """Tests the removing of the yapf enable comment"""
    string_with_yapf_enable = 'something\n# yapf: enable\notherline'
    string_without_yapf_enable = 'something\notherline'
    actual = self.helper._RemoveYapfComment(string_with_yapf_enable)
    self.assertEqual(string_without_yapf_enable, actual)

  def testRemoveYapfCommentOnlyTheDisable(self):
    """Tests the removing of the yapf enable comment"""
    string_with_yapf_enable = 'something\n# yapf: disable\notherline'
    string_without_yapf_enable = 'something\notherline'
    actual = self.helper._RemoveYapfComment(string_with_yapf_enable)
    self.assertEqual(string_without_yapf_enable, actual)

  def testRemoveYapfCommentOnlyTheEnableAndDisable(self):
    """Tests the removing of the yapf enable comment"""
    string_with_yapf_enable = ('something\n'
                               '# yapf: disable\n'
                               'otherline\n'
                               '# yapf: enable\n'
                               'lastline')
    string_without_yapf_enable = 'something\notherline\nlastline'
    actual = self.helper._RemoveYapfComment(string_with_yapf_enable)
    self.assertEqual(string_without_yapf_enable, actual)


if __name__ == '__main__':
  unittest.main()
