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

    pip install git+ssh://git@gitlab.protontech.ch/spaduraru/pyprotonrebar.git@main

Documentation
=============


To use the project:

.. code-block:: python

    import pyrackndr
    pyrackndr.CONSTANTS


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
