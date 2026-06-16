"""
DebtMirror AgentOS Integration API.
Extends GhostCFO's shared financial memory and routes cross-agent escalations.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any
from loguru import logger

router = APIRouter(prefix="/v1/agentOS/debt", tags=["AgentOS Debt Memory"])

# -------------------------------------------------------------------------
# Shared Memory Schema (Extends `agentOS:memory:financial:{user_id}`)
# -------------------------------------------------------------------------
class FinancialMemoryExtension(BaseModel):
    debt_stress_active: bool
    active_debt_cases: int
    highest_dpd: int
    total_outstanding_distressed: float
    negotiation_stage: str
    leverage_score: float
    settlement_in_progress: bool
    ombudsman_complaint_filed: bool
    estimated_settlement_savings: float
    cibil_dispute_pending: bool
    legal_action_risk: str

# -------------------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------------------

class IntakeRequest(BaseModel):
    user_id: str
    debt_description: str
    triggered_by_agent: str

@router.post("/intake")
async def trigger_intake(req: IntakeRequest):
    """
    Called proactively by GhostCFO (Day 02) when runway drops < 60 days
    and debt stress is detected. Generates initial leverage score before default.
    """
    logger.info(f"Debt Intake triggered for {req.user_id} by {req.triggered_by_agent}")
    
    # MOCK logic: runs full LangGraph intake pipeline
    return {
        "case_id": "case_9876",
        "initial_briefing": "Debt classification complete. Recommended path: Hardship Restructuring.",
        "leverage_score": 55.0
    }

@router.get("/case/{case_id}")
async def get_case_status(case_id: str):
    """
    Used by GhostCFO to track the resolution progress of distressed debt.
    """
    return {"status": "active", "stage": "counter_made", "target_savings": 150000}

@router.get("/context/{user_id}")
async def get_debt_context(user_id: str) -> Dict[str, Any]:
    """
    Used by GhostCFO for financial health calculations, and SoulMap for emotional context.
    """
    logger.info(f"Fetching Debt Context for {user_id}")
    return {
        "debt_stress_active": True,
        "highest_dpd": 120,
        "legal_action_risk": "low"
    }

class EscalationRequest(BaseModel):
    case_id: str
    reason: str
    communications_log: list

@router.post("/escalate_to_ombudsman")
async def escalate_case(req: EscalationRequest):
    """
    Called internally by DebtMirror when negotiation fails due to bank hostility.
    Prepares the evidence package and hands off to RiteOfWay (Day 06).
    """
    logger.info(f"Escalating case {req.case_id} to RiteOfWay due to: {req.reason}")
    
    evidence_package = {
        "case_summary": "Bank refused 3 formal restructuring requests.",
        "communications_log": req.communications_log,
        "regulatory_violations": ["RBI Fair Practices Code - Failure to acknowledge hardship"],
        "relief_requested": "Banking Ombudsman intervention"
    }
    
    # MOCK: await riteofway_client.submit_case(..., context=evidence_package)
    return {"status": "escalated_to_riteofway", "evidence": evidence_package}

class SettlementOutcome(BaseModel):
    lender_normalized: str
    loan_type: str
    outstanding_band: str
    dpd_at_settlement: int
    settlement_percentage: float
    negotiation_stages_used: int
    ombudsman_used: bool

@router.post("/record_outcome")
async def record_settlement_intelligence(outcome: SettlementOutcome):
    """
    Anonymized crowd-sourcing. When a case is resolved, the actual settlement
    percentage is fed back into the `LenderProfileDB` to help future borrowers.
    """
    logger.info(f"Recording anonymized settlement outcome for {outcome.lender_normalized}")
    # Inserts into postgres `lender_settlement_intel` DB
    return {"status": "intel_recorded"}
