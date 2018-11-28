# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the Timesketch sketch analyzer scaffolder."""
import unittest

from l2tscaffolder.scaffolders import timesketch_sketch


class TimesketchSketchScaffolderTest(unittest.TestCase):
  """Test class for the Timesketch sketch analyzer plugin scaffolder."""

  maxDiff = None

  def testTimesketchSketchScaffolder(self):
    """Test the Timesketch index analyzer scaffolder."""
    scaffolder = timesketch_sketch.TimesketchSketchScaffolder()
    scaffolder.SetOutputName('testing')

    file_copy_paths = [x for _, x in scaffolder.GetFilesToCopy()]
    self.assertEqual(file_copy_paths, [])

    files_generated = dict(scaffolder.GenerateFiles())

    expected_files = frozenset([
        'timesketch/lib/analyzers/testing.py',
        'timesketch/lib/analyzers/testing_test.py'])
    self.assertEqual(set(files_generated.keys()), expected_files)

    expected_init_files = frozenset([
        'timesketch/lib/analyzers/__init__.py'])
    init_generated = dict(scaffolder.GetInitFileChanges())
    self.assertEqual(set(init_generated.keys()), expected_init_files)

    expected_parser_init_addition = (
        'from timesketch.lib.analyzers import testing\n')
    self.assertEqual(
        expected_parser_init_addition,
        init_generated['timesketch/lib/analyzers/__init__.py'])

    with open('test_data/timesketch_testing_plugin.py', 'r') as fh:
      expected_parser_content = fh.read()
    self.assertEqual(
        expected_parser_content,
        files_generated['timesketch/lib/analyzers/testing_test.py'])


if __name__ == '__main__':
  unittest.main()
