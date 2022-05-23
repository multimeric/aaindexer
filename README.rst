
aaindexer
*********

A Python package for accessing and parsing the `AAindex
<https://www.genome.jp/aaindex/>`_, a collection of amino acid
properties and substitution matricies. You might want this package so
that you can characterise certain amino acid residues, for example to
compare the change in chemical properties caused by a missense
mutation. Some notable features this offers are:

*  Python API *and* CLI with JSON output

*  Detailed test suite

*  Parsing Expression Grammar for parsing aaindex entries that can be
   used independently

*  Automatic handling of some idiosyncrasies of the aaindex format

*  aaindex itself is not included, avoiding any breaches of the
   license


Installation
************

::

   pip install aaindexer

Or, if you’re a super cool `poetry <https://python-poetry.org/>`_
user:

::

   poetry add aaindexer


CLI
***


aaindexer
=========

Scrapes a single aaindex database, and prints the result to stdout. A
progress bar is shown via stderr.

.. code:: shell

   aaindexer [OPTIONS] DATABASE_NUMBER

-[ Options ]-

``--pretty, --no-pretty``

   If pretty (the default), pretty print the JSON, with newlines and
   indentation.

-[ Arguments ]-

``DATABASE_NUMBER``

   Required argument


Python API
**********

**class aaindexer.AaindexRecord**

   A single record from a single aaindex database

   ``accession: str``

      Record accession, e.g. ``"ANDN920101"``

   ``authors: Optional[str]``

      Authors for the source publication, as a single string, e.g.
      ``"Andersen, N.H., Cao, B. and Chen, C."``

   ``comment: Optional[str]``

      Additional comments

   ``correlation: Optional[dict[str, Optional[float]]]``

      A dictionary of correlations between this record and others in
      the same database. The dictionary is indexed by the record
      accession number. e.g. ``{ "ROBB760101": 0.874, "QIAN880106":
      0.846 }``

   ``description: str``

      Record description, as a string, e.g. ``"alpha-CH chemical
      shifts (Andersen et al., 1992)"``

   ``index: Optional[dict[str, Optional[float]]]``

      A dictionary indexed by amino acid 1-letter codes, where the
      values are amino acid properties described in this record. e.g.
      *{“A”: 0.68, “R”: -0.22 }`*

   ``journal: Optional[str]``

   ``matrix: Optional[dict[str, dict[str, Optional[float]]]]``

      A dictionary of dictionaries. The first and second index are
      both amino acid 1-letter codes, defining up a substitution
      matrix between the two amino acids. e.g. ``{ "A": { "A": 3.0 },
      "R": { "A": -3.0, "R": 6.0 }`` Note that if matrix[X][Y] is not
      defined, then matrix[Y][X] (the reverse) will be.

   ``pmid: Optional[str]``

      PubMed identifier, e.g. ``"PMID:1575719"``

   ``title: Optional[str]``

**aaindexer.scrape_database(index)**

   Scrapes an aaindex database, and returns it as plain text

   :Parameters:
      **index** (*int*) – The number of the database to return (1-3)

   :Returns:
      The aaindex database contents

   :Return type:
      str

**aaindexer.scrape_parse(index, progress=False)**

   Scrapes an aaindex database and parses the result

   :Parameters:
      *  **index** (*int*) – The number of the database to return
         (1-3)

      *  **progress** – If true, show progress

   :Return type:
      list[`aaindexer.models.AaindexRecord
      <#aaindexer.AaindexRecord>`_]


Development
***********

Clone the repo, and then:

*  ``poetry install`` to install development dependencies

*  ``poetry run pytest test.py`` to run tests

*  ``poetry run sphinx-build . _build -b rst`` to build the readme,
   then ``_build/index.rst README.rst`` to replace the old readme
