"""
Schemas for Negotiation Scripts.
Models the exact playbook a borrower uses during phone calls or meetings.
"""
from pydantic import BaseModel
from typing import Literal, List, Dict

class ScriptPoint(BaseModel):
    point_order: int
    topic: str
    exact_phrasing: str

class NegotiationScript(BaseModel):
    script_id: str
    debt_case_id: str
    stage: Literal["opening", "counter", "escalation"]
    channel: Literal["phone_call", "email", "in_person", "written_letter"]
    script_type: str

    opening_statement: str          # first 30 seconds
    key_points: List[ScriptPoint]   # in order of delivery
    regulatory_citations: List[str] # exact citations to have ready
    responses_to_common_tactics: Dict[str, str]  # tactic -> counter
    what_not_to_say: List[str]      # avoid these
    suggested_concessions: List[str]  # things you CAN offer
    red_lines: List[str]            # never agree to these
    closing_statement: str
    next_step_if_accepted: str
    next_step_if_rejected: str
