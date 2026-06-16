"""
CIBIL Outcomes Database.
Maps exact credit score impacts to various debt resolution paths.
"""
from pydantic import BaseModel
from typing import Dict

class CIBILOutcome(BaseModel):
    status: str
    score_impact_points: int
    recovery_timeline_months: int
    notes: str

CIBIL_OUTCOMES: Dict[str, CIBILOutcome] = {
    "paid_in_full": CIBILOutcome(
        status="Closed",
        score_impact_points=0,                 # no negative impact
        recovery_timeline_months=0,
        notes="Best outcome — full payment removes all negative history."
    ),
    "ots_settlement": CIBILOutcome(
        status="Settled",
        score_impact_points=-100,       # approximate immediate hit
        recovery_timeline_months=36,    # 3 years to recover
        notes="'Settled' stays on CIBIL for 7 years but score recovers. "
              "Better than 'Written Off'. Ask lender to mark 'Closed' "
              "instead of 'Settled' — some lenders do this for full OTS."
    ),
    "emi_restructuring": CIBILOutcome(
        status="Restructured",
        score_impact_points=-50,
        recovery_timeline_months=24,
        notes="Less damaging than settlement. Shows willingness to pay."
    ),
    "npa_sub_standard": CIBILOutcome(
        status="NPA",
        score_impact_points=-150,
        recovery_timeline_months=48,
        notes="CIBIL shows NPA with overdue amount. "
              "Settling now prevents further deterioration."
    ),
    "written_off": CIBILOutcome(
        status="Written Off",
        score_impact_points=-200,
        recovery_timeline_months=60,
        notes="Most damaging status. Banks must update to 'Settled' "
              "within 30 days of OTS completion per RBI directive."
    )
}
