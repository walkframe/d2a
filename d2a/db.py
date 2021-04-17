# coding: utf-8
import re
import logging
import warnings
from collections import OrderedDict
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker
from sqlalchemy import dialects, create_engine
from django.conf import settings
from django.db import transaction

from .compat import basestring

DIALECTS = {
    t: getattr(dialects, t).dialect
    for t in ['postgresql', 'mysql', 'oracle', 'mssql', 'sqlite', 'firebase']
    if hasattr(dialects, t)
}

EXPLAIN_PREFIXES = {
    'postgresql': 'EXPLAIN ANALYZE',
    'mysql': 'EXPLAIN',
    'oracle': 'EXPLAIN PLAN FOR',
    'sqlite': 'EXPLAIN QUERY PLAN',
}

DIALECT_MAPPING = {}

key = 'postgresql'
if key in DIALECTS:
    # https://github.com/sqlalchemy/sqlalchemy/blob/f572cdf7850b7a2ee6b7535b8129a76fa73496e6/test/sql/test_compiler.py#L2562
    DIALECT_MAPPING[DIALECTS[key]] = lambda sql, binded: (
        sql,
        binded.params,
    )

key = 'mysql'
if key in DIALECTS:
    # https://github.com/sqlalchemy/sqlalchemy/blob/f572cdf7850b7a2ee6b7535b8129a76fa73496e6/test/sql/test_compiler.py#L2583
    DIALECT_MAPPING[DIALECTS[key]] = lambda sql, binded: (
        sql,
        tuple(binded.params[k] for k in binded.positiontup),
    )

key = 'oracle'
if key in DIALECTS:
    # https://github.com/sqlalchemy/sqlalchemy/blob/f572cdf7850b7a2ee6b7535b8129a76fa73496e6/test/sql/test_compiler.py#L2569
    DIALECT_MAPPING[DIALECTS[key]] = lambda sql, binded: (
        re.sub(r"(?<!:):([A-Za-z][0-9A-Za-z_]+)", r"%(\1)s", sql),
        binded.params,
    )

key = 'sqlite'
if key in DIALECTS:
    # https://github.com/sqlalchemy/sqlalchemy/blob/f572cdf7850b7a2ee6b7535b8129a76fa73496e6/test/sql/test_compiler.py#L2599
    DIALECT_MAPPING[DIALECTS[key]] = lambda sql, binded: (
        sql.replace('?', '%s'),
        tuple(binded.params.values()),
    )

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
        'django.contrib.gis.db.backends.postgis': 'postgresql',
        'django.db.backends.mysql': 'mysql',
        'django.db.backends.oracle': 'oracle',
        'django.db.backends.sqlite3': 'sqlite3',
    }.get(settings.DATABASES[database]['ENGINE'])


def _execute_cursor(cursor, sql, params):
    try:
        cursor.execute(sql, params)
    except Exception:
        logger.exception('param:%s\nsql:%s', params, sql)


def _complement(conn, dialect, database='default'):
    if not conn:
        conn = transaction.get_connection()
    if not dialect:
        dialect = _detect_db_type(database)
    if isinstance(dialect, basestring):
        dialect = DIALECTS[dialect]

    return conn, dialect


def query_expression(stmt, conn=None, dialect=None, database='default',
                     as_col_dict=True, as_row_list=True, dict_method=OrderedDict, debug={}):
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
          %(prefix)s
        'printer': printer, # printing method. Try to use `logger.info` function for example.
        'delimiter': '=' * 100, # characters dividing debug informations.
        'database': 'default' # django database
      }
    """
    conn, dialect = _complement(conn, dialect, database)
    binded = stmt.compile(dialect=dialect())
    sql, params = DIALECT_MAPPING[dialect](str(binded), binded)
    with conn.cursor() as cursor:
        _execute_cursor(cursor, sql, params)
        if not as_col_dict:
            result = list(cursor) if as_row_list else cursor
        else:
            dicts = (dict_method(zip([c.name for c in stmt.c], row))
                     for row in cursor)
            result = list(dicts) if as_row_list else dicts

        if debug:
            show_debug(cursor, sql, params, debug)
        return result


def execute_expression(stmt, conn=None, dialect=None, database='default', debug={}):
    conn, dialect = _complement(conn, dialect, database)
    binded = stmt.compile(dialect=dialect())
    sql, params = DIALECT_MAPPING[dialect](str(binded), binded)
    with conn.cursor() as cursor:
        _execute_cursor(cursor, sql, params)
        if debug:
            show_debug(cursor, sql, params, debug)
        return cursor.rowcount


def show_debug(cursor, sql, params, options={}):
    printer = options.get('printer', print)
    delimiter = options.get('delimiter', '=' * 100 + '\n')
    database = _detect_db_type(options.get('database', 'default'))
    if options.get('show_sql', True):
        show_sql(cursor, printer, delimiter, database,
                 options.get('sql_format', False),
                 options.get('sql_reindent', True),
                 options.get('sql_keyword_case', 'upper'),
                 )

    if options.get('show_explain', False):
        show_explain(cursor, printer, delimiter, database, sql, params,
                     options.get('explain_prefix', EXPLAIN_PREFIXES[database]))


def show_sql(cursor, printer, delimiter, database, format, reindent, keyword_case):
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
            warnings.warn('Formatting sql requires "sqlparse". Do as follows: "pip install sqlparse".')
    printer(delimiter + sql)


def show_explain(cursor, printer, delimiter, database, sql, params, explain_prefix):
    explain_sql = explain_prefix + ' ' + sql
    _execute_cursor(cursor, explain_sql, params)
    sql = {
        'postgresql': lambda: '\n'.join(row[0] for row in cursor),
        'mysql': lambda: '\n'.join(' | '.join(map(str, row)) for row in cursor),
        'oracle': lambda: '\n'.join(' | '.join(map(str, row)) for row in cursor),
        'sqlite3': lambda: '\n'.join(' | '.join(map(str, row)) for row in cursor),
    }[database]()
    printer(delimiter + sql)


def make_engine(db_type=None, database='default', **options):
    uri = URI[db_type or _detect_db_type(database)]
    return create_engine(uri.format(**settings.DATABASES[database]), **options)


@contextmanager
def make_session(engine=None,
                 autoflush=True, autocommit=False,
                 expire_on_commit=True, info=None):
    engine = engine or make_engine()
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

