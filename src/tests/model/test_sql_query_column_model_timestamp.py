# !/usr/bin/python
# -*- coding: utf-8 -*-
"""test class"""
import unittest

from plasoscaffolder.model import (sql_query_column_model_timestamp)


class SQLColumnModelTimestampTest(unittest.TestCase):
  """test class for SQLColumnModel"""

  def testGetShortExpectedMessage(self):
    """Test getting the short message."""
    long_message = (
        'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam '
        'nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,'
        ' sed diam voluptua. At vero eos et accusam et justo duo dolores et ea '
        'rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem '
        'ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur '
        'sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore '
        'et dolore magna aliquyam erat, sed diam voluptua. At vero eos et '
        'accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, '
        'no sea takimata sanctus est Lorem ipsum dolor sit amet.')
    expected_message_short = '{0}...'.format(long_message[0:77])
    model = sql_query_column_model_timestamp.SQLColumnModelTimestamp(
        sql_column='not needed', sql_column_type=None, timestamp='123',
        expected_message=long_message)
    self.assertEqual(expected_message_short, model.GetShortExpectedMessage())


if __name__ == '__main__':
  unittest.main()
