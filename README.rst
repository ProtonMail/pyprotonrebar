========
Overview
========

Interact with the RackN Digital Rebar API

* Free software: Apache Software License 2.0

Installation
============

::

    pip install pyrackndr

You can also install the in-development version with::

    pip install git+ssh://git@github.com/ProtonMail/pyprotonrebar.git@main

Documentation
=============


To use the project, for example, to create a new Param:

.. code-block:: python

    import pyrackndr.pyrackndr
    TOKEN = pyrackndr.pyrackndr.fetch_token_requests(
        'superuser',
        'user:pass',
        'https://localhost:8092')
    AUTH = TOKEN['header']

    rebar_object = pyrackndr.pyrackndr.RackNDr(
        'https://localhost:8092',
        AUTH,
        'params')

    data = pyrackndr.CONSTANTS['params'].copy()
    data['Description'] = 'new-param description goes here'
    data['Documentation'] = 'new-param documentation goes here'
    data['Name'] = 'new-param'
    data['Secure'] = False
    data['Schema'] = {
      'type': 'string',
      'default': 'hello'
    }

    rebar_object.create(data)


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
