# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the Turbinia job scaffolder."""
import unittest

from l2tscaffolder.scaffolders import turbinia_job


class TurbiniaJobTaskScaffolderTest(unittest.TestCase):
  """Test class for the Turbinia job scaffolder."""

  maxDiff = None

  def testTurbiniaJobTaskScaffolder(self):
    """Test the Turbinia job scaffolder."""
    scaffolder = turbinia_job.TurbiniaJobTaskScaffolder()
    scaffolder.SetOutputName('secret_processing')

    file_copy_paths = [x for _, x in scaffolder.GetFilesToCopy()]
    self.assertEqual(file_copy_paths, [])

    files_generated = dict(scaffolder.GenerateFiles())

    expected_files = frozenset([
        'turbinia/jobs/secret_processing.py',
        'turbinia/workers/secret_processing.py',
        'turbinia/jobs/__init__.py',
        'turbinia/workers/__init__.py'])
    self.assertEqual(set(files_generated.keys()), expected_files)

    expected_parser_init_addition = (
        '# TODO: put in alphabetical order.\nfrom '
        'turbinia.jobs import secret_processing')
    self.assertEqual(
        expected_parser_init_addition,
        files_generated['turbinia/jobs/__init__.py'])

    with open('test_data/turbinia_job_output.py', 'r') as fh:
      expected_parser_content = fh.read()
    self.assertEqual(
        expected_parser_content,
        files_generated['turbinia/jobs/secret_processing.py'])


if __name__ == '__main__':
  unittest.main()
