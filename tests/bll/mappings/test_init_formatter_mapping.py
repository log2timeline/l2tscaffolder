# !/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=protected-access
# because tests should access protected members
"""test class"""
import unittest

from plasoscaffolder.bll.mappings import formatter_init_mapping
from plasoscaffolder.bll.mappings import parser_init_mapping
from plasoscaffolder.model import init_data_model
from tests.fake import fake_mapping_helper


class InitMappingTest(unittest.TestCase):
  """ Class representing tests for the init mapping"""

  def setUp(self):
    self.plugin_name = "the_one_and_only"

  def testGetFormatterInitCreate(self):
    """test the render for creating a new formatter init file"""
    mapper = formatter_init_mapping.FormatterInitMapping(
        fake_mapping_helper.FakeMappingHelper("template path"))
    data = init_data_model.InitDataModel(self.plugin_name, True)
    actual = mapper.GetRenderedTemplate(data)
    expected = "fake string formatter_init_template.jinja2"
    self.assertEqual(expected, actual)

  def testGetFormatterInitEdit(self):
    """test the render for editing a existing formatter init file"""
    mapper = formatter_init_mapping.FormatterInitMapping(
        fake_mapping_helper.FakeMappingHelper("template path"))
    data = init_data_model.InitDataModel(self.plugin_name, False)
    actual = mapper.GetRenderedTemplate(data)
    expected = "fake string formatter_init_template.jinja2"
    self.assertEqual(expected, actual)

  def testGetParserInitCreate(self):
    """test the render for creating a new parser init file"""
    mapper = parser_init_mapping.ParserInitMapping(
        fake_mapping_helper.FakeMappingHelper("template path"))
    data = init_data_model.InitDataModel(self.plugin_name, True)
    actual = mapper.GetRenderedTemplate(data)
    expected = "fake string parser_init_template.jinja2"

    self.assertEqual(expected, actual)

  def testGetParserInitEdit(self):
    """test the render for editing a existing parser init file"""
    mapper = parser_init_mapping.ParserInitMapping(
        fake_mapping_helper.FakeMappingHelper("template path"))
    data = init_data_model.InitDataModel(self.plugin_name, False)
    actual = mapper.GetRenderedTemplate(data)
    expected = "fake string parser_init_template.jinja2"
    self.assertEqual(expected, actual)


if __name__ == '__main__':
  unittest.main()
