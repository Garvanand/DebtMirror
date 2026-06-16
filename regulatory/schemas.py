"""
Schemas for the RBI Regulatory Corpus.
"""
from pydantic import BaseModel
from typing import Optional, List

class RegulatoryChunk(BaseModel):
    chunk_id: str
    document_name: str
    document_type: str          # "rbi_master_circular", "court_judgment", "bank_policy"
    circular_number: Optional[str]  # e.g., "RBI/2023-24/09"
    section_number: str
    content: str                # actual regulatory text
    plain_english_summary: str  # AI-generated summary of what this means
    applicable_to: List[str]    # ["credit_card", "personal_loan", "all"]
    borrower_benefit: str       # how borrower can use this
    citation_format: str        # exact citation string to use in documents

class RegulatoryProvision(BaseModel):
    citation_format: str
    plain_english_summary: str
    borrower_benefit: str

class BorrowerRight(BaseModel):
    category: str
    description: str
    citation_format: str

class ValidationResult(BaseModel):
    is_claim_valid: bool
    explanation: str
    refuting_citation: Optional[str]
