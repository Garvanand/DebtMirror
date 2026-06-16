"""
CIBIL Recovery Roadmap.
Generates month-by-month actionable recovery plans to eliminate the fear of permanent credit damage.
"""
from pydantic import BaseModel
from typing import List, Optional

class AccountSummary(BaseModel):
    account_type: str
    status: str

class RecoveryRoadmap(BaseModel):
    current_score: Optional[int]
    target_score_36_months: int
    month_1_to_6_plan: str
    month_6_to_18_plan: str
    month_18_to_36_plan: str
    specific_actions: List[str]

class CIBILRecoveryAdvisor:

    def generate_recovery_roadmap(
        self,
        current_score: Optional[int],
        resolution_outcome: str,
        existing_accounts: List[AccountSummary]
    ) -> RecoveryRoadmap:
        """
        Generates a predictable timeline for score recovery post-settlement or closure.
        """
        score = current_score if current_score else 550
        
        if resolution_outcome == "ots_settlement":
            target = min(750, score + 120)
            m1_6 = "Score stabilizes. The heavy point drops stop as DPD stops accumulating. Ensure the lender updates the status from 'Written Off' to 'Settled'."
        else:
            target = min(800, score + 180)
            m1_6 = "Score stabilizes. The account will reflect 'Closed'. Minor recovery begins immediately."
            
        return RecoveryRoadmap(
            current_score=current_score,
            target_score_36_months=target,
            month_1_to_6_plan=m1_6,
            month_6_to_18_plan="Score gradually improves. Existing positive accounts carry more weight.",
            month_18_to_36_plan=f"The negative impact of the '{'Settled' if resolution_outcome == 'ots_settlement' else 'Closed'}' status significantly reduces.",
            specific_actions=[
                "Open a secured credit card (FD-backed) to rebuild positive repayment history.",
                "Keep credit utilization strictly below 30% on all active accounts.",
                "Never miss an EMI again.",
                "Pull a fresh CIBIL report in 45 days to verify the bank correctly reported your resolution."
            ]
        )
