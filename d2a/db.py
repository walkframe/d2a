# coding: utf-8
import re
import logging
import warnings
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from django.conf import settings
from django.db import transaction

from .compat import basestring

EXPLAIN_PREFIXES = {
    'postgresql': 'EXPLAIN ANALYZE',
    'mysql': 'EXPLAIN',
    'oracle': 'EXPLAIN PLAN FOR',
    'sqlite': 'EXPLAIN QUERY PLAN',
}


MS_DSN = 'DRIVER={{SQL Server}}; SERVER={HOST}; DATABASE={NAME}; UID={USER}; PWD={PASSWORD};'
URI = {
    'postgresql': 'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
    'postgresql+psycopg2': 'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}', 
    'mysql': 'mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
    'mysql+mysqldb': 'mysql+mysqldb://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
    'oracle': 'oracle://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
    'oracle+cx_oracle': 'oracle+cx_oracle://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
    'mssql': 'mssql://{USER}:{PASSWORD}@' + MS_DSN,
    'mssql+pyodbc': 'mssql+pyodbc://{USER}:{PASSWORD}@' + MS_DSN,
    'mssql+adodbapi': 'mssql+adodbapi://{USER}:{PASSWORD}@' + MS_DSN,
    'mssql+pymssql': 'mssql+pymssql://{USER}:{PASSWORD}@' + MS_DSN,
    'sqlite': 'sqlite:///{NAME}',
    'sqlite3': 'sqlite:///{NAME}',
    'sqlite+memory': 'sqlite://',
}

logger = logging.getLogger(__name__)


def _detect_db_type(database='default'):
    return {
        'django.db.backends.postgresql': 'postgresql',
        'django.db.backends.postgresql_psycopg2': 'postgresql',
        'django.db.backends.mysql': 'mysql',
        'django.db.backends.oracle': 'oracle',
        'django.db.backends.sqlite3': 'sqlite3',
    }.get(settings.DATABASES[database]['ENGINE'])


def query_expression(stmt, engine=None, database='default',
                     as_col_dict=True, as_row_list=True, dict_method=dict, debug={}):
    """
    :stmt: sqlalchemy expression object
    :as_col_dict: 
      default: True,
    :as_row_list:
      default: True,
    :debug: 
      default: {
        'show_sql': True, # if showing the sql query or not.
        'show_explain': False, # if showing explain for the sql query or not.
        'sql_format': False, # if formatting the sql query or not.
        'sql_reindent': True, # if setting indent the sql query or not.
        'sql_keyword_case': 'upper', # A rule converting reserved words.
        'explain_prefix': depends on the database type. unless you specify it, it is automatically used the following:
          'postgresql': 'EXPLAIN ANALYZE',
          'mysql': 'EXPLAIN',
          'oracle': 'EXPLAIN PLAN FOR',
          'sqlite': 'EXPLAIN QUERY PLAN',
        'printer': logger.debug, # printing method, if you use python3, then try to use `print` function.
        'delimiter': '=' * 100, # characters dividing debug informations.
        'database': 'default' # django database
      }
    """
    engine = engine or make_engine(database=database)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        if debug:
            with conn.connection.cursor() as cursor:
                show_debug(cursor, {**debug, 'database': database})

    if not as_col_dict:
        rows = list(result) if as_row_list else result
    else:
        dicts = (
            dict_method(zip([c.name for c in stmt.c], row))
            for row in result
        )
        rows = list(dicts) if as_row_list else dicts
    return rows


def execute_expression(stmt, engine=None, database='default', debug={}):
    engine = engine or make_engine(database=database)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        if debug:
            with conn.connection.cursor() as cursor:
                show_debug(cursor, {**debug, 'database': database})
    return result.rowcount


def show_debug(cursor, options={}):
    printer = options.get('printer', print)
    delimiter = options.get('delimiter', '=' * 100 + '\n')
    database = _detect_db_type(options.get('database', 'default'))
    sql = get_sql(cursor, printer, delimiter, database,
                  options.get('sql_format', False),
                  options.get('sql_reindent', True),
                  options.get('sql_keyword_case', 'upper'))

    if options.get('show_sql', True):
        printer(sql)

    if options.get('show_explain', False):
        show_explain(cursor, sql, printer, delimiter, database,
                     options.get('explain_prefix', EXPLAIN_PREFIXES[database]))


def get_sql(cursor, printer, delimiter, database, format, reindent, keyword_case):
    sql = {
        'postgresql': lambda: cursor.db.queries_log[-1]['sql'],
        'mysql': lambda: cursor.db.queries_log[-1]['sql'],
        'oracle': lambda: cursor.db.queries_log[-1]['sql'],
        'sqlite3': lambda: cursor.db.queries_log[-1]['sql'],
    }[database]()
    if format:
        try:
            import sqlparse
            sql = sqlparse.format(sql, reindent=reindent, keyword_case=keyword_case)
        except ImportError:
            warnings.warn('Formatting sql requires "sqlparse". Install as follows: "pip install sqlparse".')
    return sql


def show_explain(cursor, printer, delimiter, database, sql, params, explain_prefix):
    explain_sql = explain_prefix + ' ' + sql
    cursor.execute(explain_sql)
    result = {
        'postgresql': lambda: '\n'.join(row[0] for row in cursor),
        'mysql': lambda: '\n'.join(' | '.join(map(str, row)) for row in cursor),
        'oracle': lambda: '\n'.join(' | '.join(map(str, row)) for row in cursor),
        'sqlite3': lambda: '\n'.join(' | '.join(map(str, row)) for row in cursor),
    }[database]()
    printer(delimiter + result)


def make_engine(db_type=None, database='default', encoding='utf8', echo=False):
    uri = URI[db_type or _detect_db_type(database)]
    return create_engine(
        uri.format(**settings.DATABASES[database]),
        encoding=encoding, echo=echo)


@contextmanager
def make_session(engine=None,
                 autoflush=True, autocommit=False,
                 expire_on_commit=True, info=None):
    if not engine:
        engine = make_engine()
    Session = sessionmaker(engine,
                           autoflush=autoflush, autocommit=autocommit,
                           expire_on_commit=expire_on_commit, info=info)
    session = Session()
    try:
        yield session
    except Exception:
        session.rollback()
        logger.exception('An error occured during executing the statements.')
    else:
        if not autoflush:
            session.flush()
        if not autocommit:
            session.commit()
    finally:
        session.close()


AUTO_DETECTED_DB_TYPE = _detect_db_type()

