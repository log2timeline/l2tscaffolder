# -*- coding: utf-8 -*-
"""Tests for the Turbinia job and task scaffolder."""
import unittest

from l2tscaffolder.scaffolders import turbinia_job_task


class TurbiniaJobTaskScaffolderTest(unittest.TestCase):
  """Test class for the Turbinia job and task scaffolder."""

  maxDiff = None

  def testTurbiniaJobTaskScaffolder(self):
    """Test the Turbinia job and task scaffolder."""
    scaffolder = turbinia_job_task.TurbiniaJobTaskScaffolder()
    scaffolder.SetOutputName('secret_processing')

    file_copy_paths = [x for _, x in scaffolder.GetFilesToCopy()]
    self.assertEqual(file_copy_paths, [])

    files_generated = dict(scaffolder.GenerateFiles())

    expected_files = frozenset([
        'turbinia/jobs/secret_processing.py',
        'turbinia/workers/secret_processing.py'])
    self.assertEqual(set(files_generated.keys()), expected_files)

    expected_init_files = frozenset([
        'turbinia/jobs/__init__.py'])
    init_generated = dict(scaffolder.GetInitFileChanges())
    self.assertEqual(set(init_generated.keys()), expected_init_files)

    with open('test_data/turbinia_job_output.py', 'r') as fh:
      expected_parser_content = fh.read()
    self.assertEqual(
        expected_parser_content,
        files_generated['turbinia/jobs/secret_processing.py'])


if __name__ == '__main__':
  unittest.main()
