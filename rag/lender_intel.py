"""
Lender Settlement Intelligence API.
Retrieves historical crowd-sourced averages to give borrowers an information advantage.
"""
from loguru import logger
from typing import Optional

class LenderIntelDB:

    async def get_settlement_range(self, lender_name: str, loan_type: str, dpd: int) -> dict:
        """
        Determines the realistic boundary of what a specific lender will accept based on DPD.
        """
        logger.info(f"Fetching settlement intel for {lender_name} ({loan_type}) at {dpd} DPD.")
        
        # MOCK IMPLEMENTATION (In production, hits postgres `lender_settlement_intel`)
        if loan_type == "credit_card" and dpd >= 90:
            return {
                "avg_settlement_pct": 0.35, # Bank settles for 35% of outstanding
                "range_min": 0.25,
                "range_max": 0.45,
                "escalation_sensitivity": True, # Escalating to Nodal Officer works well
                "behavioral_note": "They typically start by demanding 80%. Hold firm. Do not pay 'token' amounts."
            }
        elif loan_type == "personal_loan" and dpd < 90:
            return {
                "avg_settlement_pct": 0.0, # Pre-NPA, they won't settle principle
                "range_min": 0.0,
                "range_max": 0.0,
                "escalation_sensitivity": False,
                "behavioral_note": "Pre-NPA status. Target EMI restructuring or waiver of penal charges, not principle settlement."
            }
            
        return {
            "avg_settlement_pct": 0.50,
            "range_min": 0.40,
            "range_max": 0.60,
            "escalation_sensitivity": False,
            "behavioral_note": "Standard recovery protocols apply."
        }
