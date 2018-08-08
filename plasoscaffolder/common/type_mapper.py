# -*- coding: utf-8 -*-
"""The mapper between SQL and python data types"""


class TypeMapperSQLitePython(object):
  """The mapper between SQLite and python data types

  The mappings taken from the site: https://sqlite.org/datatype3.html
  """
  MAPPINGS = {'BLOB': bytes,
              'INTEGER': int,
              'INT': int,
              'TINYINT': int,
              'SMALLINT': int,
              'MEDIUMINT': int,
              'BIGINT': int,
              'UNSIGNED BIG INT': int,
              'INT2': int,
              'INT8': int,
              'CHARACTER': str,
              'CHAR': str,
              'VARCHAR': str,
              'VARYING CHARACTER': str,
              'NCHAR': str,
              'NATIVE CHARACTER': str,
              'NVARCHAR': str,
              'TEXT': str,
              'CLOB': str,
              'STRING': str,
              'REAL': float,
              'DOUBLE': float,
              'DOUBLE PRECISION': float,
              'FLOAT': float,
              'NUMERIC': int,
              'DECIMAL': int,
              'BOOLEAN': bool,
              'DATE': int,
              'DATETIME': int}
