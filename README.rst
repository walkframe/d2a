.. image:: https://badge.fury.io/py/d2a.svg
  :target: https://badge.fury.io/py/d2a

.. image:: https://github.com/walkframe/d2a/workflows/master/badge.svg)]
  :targe: https://github.com/walkframe/d2a/actions



Requirements
============
- Python: 3.5 or later.

  - Tested with 3.5.7, 3.8.0

- Django: 1.11, 2.x, 3.x
  
  - Tested with 1.11.27, 2.2.9, 3.0.1

- SQLAlchemy: 1.1 or later.

  - Tested with 1.1.0, 1.3.12

Installation
============

.. code:: bash

  $ pip install d2a

Usage
=====

Auto loading
------------
Just add `d2a` to ``settings.INSTALLED_APPS``.

.. code-block:: python

  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
  
      # top or here
      'd2a',

      # example apps
      'books',
      'sales',
  ]

.. warning::

  Put it before apps you made as you can.
  Because it expects to register alchemy model before the other ``apps.py``.

Then `models_sqla` (default) in all apps will be imported as a module.

.. code:: python

  >>> from books import models_sqla
  >>> models_sqla.  # tab completion
  models_sqla.Author(            models_sqla.BookCategory(      models_sqla.CategoryRelation(  models_sqla.transfer(
  models_sqla.Book(              models_sqla.Category(          models_sqla.models
  
  >>> models_sqla.Book
  <class 'd2a.book'>
  
  >>> models_sqla.Book.  # tab completion
  models_sqla.Book.author       models_sqla.Book.content      models_sqla.Book.metadata     models_sqla.Book.tags
  models_sqla.Book.author_id    models_sqla.Book.description  models_sqla.Book.mro(         models_sqla.Book.title
  models_sqla.Book.category     models_sqla.Book.id           models_sqla.Book.price
  # SQL Expression schema
  >>> models_sqla.Book.__table__
  Table(
    'book', MetaData(bind=None), 
    Column('id', UUID(), table=<book>, primary_key=True, nullable=False, default=ColumnDefault(<function uuid4 at 0x7f3cebe7e598>)), 
    Column('price', JSON(astext_type=Text()), table=<book>, nullable=False), 
    Column('title', VARCHAR(length=255), table=<book>, nullable=False), 
    Column('description', TEXT(), table=<book>),
    Column('author_id', INTEGER(), ForeignKey('author.id'), table=<book>), 
    Column('content', BYTEA(), table=<book>, nullable=False), 
    Column('tags', ARRAY(VARCHAR()), table=<book>, nullable=False), 
    schema=None
  )

Also, it can extract model declared implicitly depending on m2m field.
(in this case, `BookCategory`)

.. note::

  You can set configrations to ``settings.py``.

  Example:

  .. code-block:: python

    # This variable can be omitted.
    D2A_CONFIG = {
        'AUTOLOAD': { # optional
            # module name: It can be used different module name from `models_sqla`.
            'module': 'modelsa',  # optional, default: 'models_sqla'
            # waiting seconds during autoloading
            'seconds': 5,  # default: 1
            # transfer function's args after 'exports' arg.
            'option': {  # optional
                'db_type': 'postgresql',  # default: 'default'
                'back_type': 'backref',  # default: 'backref'
                'as_table': True,  # default: False
                'name_formatter': str.upper,  # default: get_camelcase
            }
        },
        # converting rules for customized fields
        'ALIASES': {  # optional
            # Evaluates ExtendedImageField as ImageField
            ExtendedImageField: models.ImageField,
        },
    }


Per models module
-----------------
If you want to create a module manually, create a `models_sqla.py` in the apps.

Write like the following to it:

.. code-block:: python3

  from d2a import transfer
  from . import models
  transfer(models, globals())

`models_sqla.py` exists, auto module creation will be omitted.

And if you create every `models_sqla.py` manually,
it is unnecessary to set `d2a` to ``settings.INSTALLED_APPS``.

Example:

- `project_postgresql/books/models_sqla.py <https://github.com/walkframe/d2a/blob/master/project_postgresql/books/models_sqla.py>`_
- You can omit specifying `db_type`, then it automatically detects a database type from ``settings.DATABASES['default']``.

  - Now `postgresql`, `mysql` and `oracle` are allowed,
    the other types will be converted to the following types as ``default`` type: 
    `sqlalchemy/types.py <https://github.com/zzzeek/sqlalchemy/blob/master/lib/sqlalchemy/types.py>`_

Per model
---------
If you just want to convert one model, you should use `declare` function.

.. code:: python

  >>> from d2a import declare
  >>> from sales.models import Sales
  >>> sales = declare(Sales)
  >>> sales
  <class 'd2a.sales'>
  
  >>> sales.__table__
  Table(
    'sales', MetaData(bind=None), 
    Column('id', BIGINT(), table=<sales>, primary_key=True, nullable=False), 
    Column('book_id', UUID(), ForeignKey('book.id'), table=<sales>, nullable=False), 
    Column('sold', TIMESTAMP(), table=<sales>, nullable=False), 
    Column('reservation', INTERVAL(), table=<sales>), 
    Column('source', INET(), table=<sales>), 
    schema=None
  )
  
  >>> sales.
  sales.book         sales.id           sales.mro(         sales.sold
  sales.book_id      sales.metadata     sales.reservation  sales.source


Custom fields
-------------
If you are using customized field (not built-in),
you can register the field as the other field using `alias` or `alias_dict` method.

.. code:: python

  from django.db.models import ImageField
  
  class ExtendedImageField(ImageField):
      """something customizing"""
  
  from d2a import alias
  alias(ExtendedImageField, ImageField)

  # or
  alias_dict({
      ExtendedImageField: ImageField,
  })


.. note::

  Before 2.1.x d2a maps ``django.contrib.postgres.fields.JSONField`` to ``JSON`` uncorrectly. It should have mapped it to ``JSONB``.

  Since 2.2.0 the mapping is fixed.

  If you want to use ``JSON` type as before, then you are able to map some jsonfield to ``JSON` as follows:
  
  .. code-block:: python3
  
    from jsonfield import JSONField  # e.g. https://github.com/dmkoch/django-jsonfield
    import d2a

    d2a.alias(JSONField, d2a.JSONType)

  Or add to ``settings.D2A_CONFIG['ALIASES']``.


Querying shortcut
------------------
ORM
~~~~~~~~~~~~~~~~~~
There is a function named `make_session` for ORM mode.

.. code-block:: python3

  >>> from d2a import make_session
  >>> from books.models_sqla import Author
  
  >>> with make_session() as session:
  ...     # it commits and flushes automatically when the scope exits.
  ...     a = Author()
  ...     a.name = 'righ'
  ...     a.age = 30
  ...     session.add(a)
  ...
  >>> with make_session() as session:
  ...     # when the session was rolled back or causes some exception in the context,
  ...     # it won't register records in the session.
  ...     a = Author()
  ...     a.name = 'teruhiko'
  ...     a.age = 85
  ...     session.add(a)
  ...     session.rollback()
  ...
  >>> with make_session() as session:
  ...     session.query(Author.name, Author.age).all()
  ...
  [('righ', 30)]

It receives the following arguments:

:engine: engine object or database-type (**string**) (default: None). When it is omitted, it guesses database type and gets an engine automatically.
:autoflush: It is the same as `sessionmaker <https://docs.sqlalchemy.org/en/latest/orm/session_api.html#session-and-sessionmaker>`__ (default: True)
:autocommit:  It is the same as `sessionmaker <https://docs.sqlalchemy.org/en/latest/orm/session_api.html#session-and-sessionmaker>`__ (default: False)
:expire_on_commit: It is the same as `sessionmaker <https://docs.sqlalchemy.org/en/latest/orm/session_api.html#session-and-sessionmaker>`__ (default: True)
:info: It is the same as `sessionmaker <https://docs.sqlalchemy.org/en/latest/orm/session_api.html#session-and-sessionmaker>`__ (default: None)

All arguments can be omitted.

Expression
~~~~~~~~~~~~~~~~~~
There are two functions.

:query_expression: To retrieve `SELECT` results, and returns a list containing record.
:execute_expression: To execute `INSERT`, `DELETE`, `UPDATE` statements, and returns num of records having been affected.

.. code-block:: python3

  >>> from sqlalchemy import (
  ...     select,
  ...     insert,
  ... )
  
  >>> from d2a import query_expression, execute_expression

  # if you try on `project_mysql` demo, you should write ``from books.modelsa import Author``
  >>> from books.models_sqla import Author
  
  >>> AuthorTable = Author.__table__
  
  >>> records = [
  ...     {'name': 'a', 'age': 10},
  ...     {'name': 'b', 'age': 30},
  ...     {'name': 'c', 'age': 20},
  ... ]
  
  >>> # insert
  >>> stmt = insert(AuthorTable).values(records)
  >>> execute_expression(stmt)
  3
  
  >>> # select
  >>> stmt = select([
  ...     AuthorTable.c.id,
  ...     AuthorTable.c.name,
  ...     AuthorTable.c.age,
  ... ]).select_from(AuthorTable).order_by(AuthorTable.c.age)

  >>> query_expression(stmt)
  [
    OrderedDict([('id', 12), ('name', 'a'), ('age', 10)]),
    OrderedDict([('id', 14), ('name', 'c'), ('age', 20)]),
    OrderedDict([('id', 13), ('name', 'b'), ('age', 30)])
  ]

  >>> # record as tuple
  >>> query_expression(stmt, as_col_dict=False)
  [(12, 'a', 10), (14, 'c', 20), (13, 'b', 30)]

  >>> query_expression(stmt, as_col_dict=False, debug={'printer': print, 'show_explain': True, 'sql_format': True})
  ====================================================================================================
  SELECT author.id,
         author.name,
         author.age
  FROM author
  ORDER BY author.age
  ====================================================================================================
  Sort  (cost=16.39..16.74 rows=140 width=522) (actual time=0.027..0.028 rows=18 loops=1)
    Sort Key: age
    Sort Method: quicksort  Memory: 25kB
    ->  Seq Scan on author  (cost=0.00..11.40 rows=140 width=522) (actual time=0.007..0.009 rows=18 loops=1)
  Planning time: 0.072 ms
  Execution time: 0.047 ms
  [(12, 'a', 10), (14, 'c', 20), (13, 'b', 30)]

.. note::

  I added argument of ``query_expression()`` to see debugging information.

  Specify options as dict type like the following:

  .. code-block:: python3

    query_expression(stmt, debug={  # all options can be skipped.
        'show_sql': True, # if showing the sql query or not.
        'show_explain': False, # if showing explain for the sql query or not.
        'sql_format': False, # if formatting the sql query or not.
        'sql_reindent': True, # if setting indent the sql query or not.
        'sql_keyword_case': 'upper', # A rule converting reserved words.
        'explain_prefix': depends on the database type. unless you specify it, an appropriate prefix will be automatically used.
        'printer': logger.debug, # printing method, if you use python3, then try `print` function.
        'delimiter': '=' * 100, # characters dividing debug informations.
        'database': 'default' # django database
    })

  Default is ``{}`` (An empty dict means disabling debug.)

.. warning::

  Supported auto-detecting db types are the following:
  
  - PostgreSQL
  - MySQL
  - Oracle

Demo
============

start up environment
--------------------

.. code-block:: shell

  $ git clone git@github.com:walkframe/d2a.git
  $ cd d2a
  $ docker-compose up

preparation
--------------------

.. code-block:: shell 

  $ docker exec -it d2a_app /bin/bash
  # python -m venv venv # only first time
  # source venv/bin/activate
  (venv) # cd project_postgresql/ # (or mysql)
  (venv) project_postgresql # ./manage.py migrate

execute
------------

.. code-block:: shell

  (venv) project_postgresql # ./manage.py shell

.. code-block:: python

  >>> from books import models_sqla
  >>> book = models_sqla.Book()
  >>> author = models_sqla.Author()
  >>> book.author = author
  >>> author.books
  [<d2a.book object at 0x7f3cec539358>]
  # And do something you want to do ;)


Links
=====
- https://github.com/walkframe/d2a
- https://pypi.org/project/d2a/

History
=======
:2.2.x:

  - Supported the following fields:

    - `PositiveBigInteger`
    - `SmallAutoField`

  - Dropped support for the following versions:

    - Python: `< 3.5.0`.
    - SQLAlchemy: `< 1.1.0`.

  - ``d2a.make_engine`` can receive all ``create_engine`` arguments now.
  - Remapped django JSONField to JSONB (it was ``JSON`` before)
  - Migrated to GitHub Actions from CircleCI.


:2.1.0:

  - Changed: 
  
    - **Warning:** Changed arg name ``as_dict`` to ``as_col_dict``
  
  - Added:
    
    :as_row_list: 
      
      If result set being list type or not.
    
      default is ``True``.
    
    :dict_method:
    
      A method making row to dict.
      You got to be able to change the method to ``dict()``.

      default is ``collections.OrderedDict``.

    :debug:
      
      If showing debug information or not. specify options dict.

:2.0.0:

  - Added a shortcut function for executing in ORM mode.
  - Added two shortcut functions for executing in EXPRESSION mode.

:1.1.x:

  - (2019-02-17)
  - Added a function to load all models automatically.

:1.0.2:
  
  - (2018-07-10)
  - Improved a little.

:1.0.1:

  - (2018-07-06)
  - Fixed a bug, that it will be provided `None` even though it's not specified `default` argument.

:1.0.0:

  - (2018-07-05)
  - Fixed bugs.
  - Added unit tests.

:0.0.6:

  - Fixed a bug that abstract models become the targets.
  - Deleted `install_requires`.

:0.0.5:

  - added alias method.

:0.0.4:

  - fixed bugs.

:0.0.3:

  - it got easy to declare custom field.
  - transfer method can define secondary table.

:0.0.2:

  - it supported m2m field.
  - it limited django version less than `1.9`.

:0.0.1: first release (2017-12-27)
