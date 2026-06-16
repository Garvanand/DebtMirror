"""
Pydantic v2 Models for DebtMirror.
Models borrower profiles, negotiation state, and lender intelligence.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Literal, List
from datetime import datetime

class DebtProfile(BaseModel):
    case_id: str
    user_id: str
    lender_name: str
    loan_type: Literal["credit_card", "personal_loan", "education_loan", "home_loan", "msme"]
    outstanding_amount: float
    dpd: int = Field(..., ge=0, description="Days Past Due")
    cibil_score: Optional[int] = Field(None, ge=300, le=900)
    
    # Computed leverage score (0-100)
    leverage_score: float = 0.0
    optimal_path: Optional[str] = None

class NegotiationStage(BaseModel):
    case_id: str
    current_stage: Literal["intake", "pre_npa_negotiation", "ots_proposal", "ombudsman_escalation"]
    last_lender_communication: Optional[str]
    last_updated_at: datetime = Field(default_factory=datetime.utcnow)

class LenderIntelligence(BaseModel):
    lender_name: str
    loan_type: str
    dpd_range_start: int
    dpd_range_end: int
    avg_settlement_percentage: float = Field(..., ge=0.0, le=1.0)
    escalation_sensitivity: bool

class ResolutionStrategy(BaseModel):
    case_id: str
    target_settlement_amount: float
    cibil_impact_warning: str
    strategy_steps: List[str]
    regulatory_citations: List[str]
    legal_disclaimer: str = (
        "This is informational guidance based on publicly available RBI regulations. "
        "For complex debt matters, consult a qualified advocate or CIBIL-certified credit counselor."
    )
