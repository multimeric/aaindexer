from pydantic import BaseModel
from typing import Optional


class AaindexRecord(BaseModel):
    accession: str
    description: str
    pmid: Optional[str]
    authors: Optional[str]
    title: Optional[str]
    journal: Optional[str]
    comment: Optional[str]
    correlation: Optional[dict[str, Optional[float]]]
    index: Optional[dict[str, Optional[float]]]
    matrix: Optional[dict[str, dict[str, Optional[float]]]]
