"""
Pydantic classes
"""
from pydantic import BaseModel
from typing import Optional


class AaindexRecord(BaseModel):
    """
    A single record from a single aaindex database
    """
    #: Record accession, e.g. ANDN920101
    accession: str
    #: Record description, as a string
    description: str
    #: PubMed identifier
    pmid: Optional[str]
    #: Authors for the source publication, as a single string
    authors: Optional[str]
    #: Title of the source publication
    title: Optional[str]
    #: Journal for the source publication
    journal: Optional[str]
    #: Additional comments
    comment: Optional[str]
    #: A correlation matrix between this record and others in the same database
    correlation: Optional[dict[str, Optional[float]]]
    #: A dictionary indexed by amino acid 1-letter codes, where the values are
    #: amino acid properties described in this record
    index: Optional[dict[str, Optional[float]]]
    #: A dictionary of dictionaries. The first and second index are both amino acid
    #: 1-letter codes, defining up a substitution matrix between the two amino acids.
    #: Note that if matrix[X][Y] is not defined, then matrix[Y][X] (the reverse) will be
    matrix: Optional[dict[str, dict[str, Optional[float]]]]
