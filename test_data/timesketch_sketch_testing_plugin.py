"""Tests for TestingPlugin."""

import mock

from timesketch.lib.analyzers import testing
from timesketch.lib.testlib import BaseTest
from timesketch.lib.testlib import MockDataStore


class TestTesting(BaseTest):
    """Tests the functionality of the analyzer."""

    @mock.patch(
        u'timesketch.lib.analyzers.interface.OpenSearchDataStore',
        MockDataStore)
    def setUp(self):
        """Setup for for running the Testing analyzer tests."""
        super().setUp()

    # Mock the Opensearch datastore.
    @mock.patch(
        u'timesketch.lib.analyzers.interface.OpenSearchDataStore',
        MockDataStore)
    def test_Testing_analyzer_class(self):
        """Test core functionality of the analyzer class."""
        # TODO: Write actual tests here.
        self.assertEqual(True, False)
