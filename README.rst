.. image:: https://badge.fury.io/py/d2a.svg
  :target: https://badge.fury.io/py/d2a

.. image:: https://github.com/walkframe/d2a/workflows/build/badge.svg?branch=master
  :target: https://github.com/walkframe/d2a/actions

.. image:: https://img.shields.io/pypi/dm/d2a.svg
  :target: https://pypi.org/project/d2a/

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
  :target: https://opensource.org/licenses/MIT

Requirements
============
- Python: 3.5 or later.

  - Tested with 3.6, 3.9

- Django: 2.x, 3.x
  
  - Tested with 2.2.9, 3.0.1, 3.1.1

- SQLAlchemy: 1.1 or later.

  - Tested with 1.1.0, 1.4.1

2 STEPS TO USE
==============

Installation
-------------

.. code-block:: shell

  $ pip install d2a -U


Add d2a to settings.INSTALLED_APPS.

.. code-block:: python3

  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      # :
      # :
      'd2a',
  ]

Code generation
---------------

.. code-block:: shell

  $ ./manage.py sqla_codegen


Link
==================

- `PyPI <https://pypi.org/project/d2a>`__
- See more details on `walkframe docs <https://docs.walkframe.com/products/d2a/>`__

  - `History <https://docs.walkframe.com/products/d2a/history/>`__
