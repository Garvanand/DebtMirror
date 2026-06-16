"""
Lender Profile Intelligence DB.
Crowd-sourced, anonymized database of lender settlement behaviors.
"""
from pydantic import BaseModel
from typing import List, Tuple, Optional

class AuthorityLevel(BaseModel):
    level: str
    max_amount: Optional[float]

class LenderProfile(BaseModel):
    lender_id: str
    lender_type: str
    typical_settlement_range: Tuple[float, float]
    settlement_authority_levels: List[AuthorityLevel]
    preferred_contact: str
    ombudsman_response_rate: float
    typical_response_days: int
    known_tactics: List[str]

class LenderProfileDB:
    LENDER_PROFILES = {
        "hdfc_bank": LenderProfile(
            lender_id="hdfc_bank",
            lender_type="private_sector_bank",
            typical_settlement_range=(0.65, 0.85),  # 65-85% of outstanding
            settlement_authority_levels=[
                AuthorityLevel(level="branch", max_amount=500000),
                AuthorityLevel(level="zonal", max_amount=2000000),
                AuthorityLevel(level="head_office", max_amount=None)
            ],
            preferred_contact="grievance.officer@hdfcbank.com",
            ombudsman_response_rate=0.85,
            typical_response_days=15,
            known_tactics=[
                "Initial offers are always below authority ceiling",
                "Zonal escalation almost always produces better terms",
                "Year-end (March) offers improve significantly"
            ]
        ),
        "sbi": LenderProfile(
            lender_id="sbi",
            lender_type="public_sector_bank",
            typical_settlement_range=(0.50, 0.70),
            settlement_authority_levels=[
                AuthorityLevel(level="branch", max_amount=200000),
                AuthorityLevel(level="zonal", max_amount=1000000),
                AuthorityLevel(level="head_office", max_amount=None)
            ],
            preferred_contact="contactcentre@sbi.co.in",
            ombudsman_response_rate=0.90,
            typical_response_days=21,
            known_tactics=[
                "Highly sensitive to NPA provisioning rules",
                "Slow to respond until Ombudsman is cc'd",
                "Rarely waive principle, but heavily waive penal interest"
            ]
        ),
        "bajaj_finance": LenderProfile(
            lender_id="bajaj_finance",
            lender_type="nbfc",
            typical_settlement_range=(0.40, 0.60),
            settlement_authority_levels=[
                AuthorityLevel(level="branch", max_amount=100000),
                AuthorityLevel(level="zonal", max_amount=None)
            ],
            preferred_contact="wecare@bajajfinserv.in",
            ombudsman_response_rate=0.75,
            typical_response_days=10,
            known_tactics=[
                "Aggressive early-stage recovery tactics",
                "High willingness to settle at deep discounts post-180 DPD",
                "Often employ third-party agencies violating 0700-1900 hours rule"
            ]
        )
    }

    def get_profile(self, lender_id: str) -> Optional[LenderProfile]:
        return self.LENDER_PROFILES.get(lender_id.lower())
