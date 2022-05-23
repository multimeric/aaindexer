aaindexer
=========

A Python package for accessing and parsing the `AAindex <https://www.genome.jp/aaindex/>`_, a collection of amino acid properties and substitution matricies.
You might want this package so that you can characterise certain amino acid residues, for example to compare the change in chemical properties caused by a missense mutation.
Some notable features this offers are:

* Python API *and* CLI with JSON output
* Detailed test suite
* Parsing Expression Grammar for parsing AAindex entries that can be used independently
* Automatic handling of some idiosyncrasies of the AAindex format
* AAindex itself is not included, avoiding any breaches of the license

Installation
============

::

   pip install aaindexer

Or, if you're a super cool `poetry <https://python-poetry.org/>`_ user:

::

   poetry add aaindexer

CLI
===

.. click:: aaindexer.cli:main
   :prog: aaindexer
   :nested: full

Python API
==========

.. automodule:: aaindexer
   :imported-members:
   :members:
   :undoc-members:

Citation
========

Please cite the original AAindex paper if you are using this package or the raw data:
Kawashima, S. & Kanehisa, M. AAindex: Amino Acid index database. Nucleic Acids Research 28, 374 (2000).

Development
===========

Clone the repo, and then:

* ``poetry install`` to install development dependencies
* ``poetry run pytest test.py`` to run tests
* ``poetry run sphinx-build . _build -b rst`` to build the readme, then ``_build/index.rst README.rst`` to replace the old readme
