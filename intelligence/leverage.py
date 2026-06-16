"""
Borrower Leverage Engine.
The most important output: Calculates exactly how much negotiating power the borrower has.
"""
from pydantic import BaseModel
from typing import Dict
from .classification import DebtClassification
from .lender_db import LenderProfile

class LeverageAnalysis(BaseModel):
    leverage_score: float
    leverage_breakdown: Dict[str, float]
    key_leverage_points: list[str]

class SettlementRange(BaseModel):
    aggressive_ask: float
    realistic_target: float
    walk_away_point: float
    rationale: str

class BorrowerLeverageEngine:

    def calculate_leverage_score(
        self,
        debt_profile: DebtClassification,
        lender_profile: LenderProfile
    ) -> LeverageAnalysis:
        """
        Scores borrower leverage out of 100 based on 5 parameters.
        """
        score = 0.0
        breakdown = {}
        points = []

        # 1. NPA Pressure Score (0-30)
        dpd = debt_profile.months_overdue * 30
        if 60 <= dpd <= 89:
            npa_score = 25.0
            points.append("Bank is in the Golden Window (SMA-1) and highly motivated to avoid imminent NPA provisioning.")
        elif 90 <= dpd <= 119:
            npa_score = 30.0
            points.append("Account just hit NPA. Branch managers are under intense pressure to cure the account.")
        elif dpd > 360:
            npa_score = 15.0
            points.append("Account is an old NPA. Immediate branch pressure is gone, but recovery ops will accept heavy discounts.")
        else:
            npa_score = 0.0
            points.append("Bank feels no NPA pressure currently.")
        breakdown["npa_pressure"] = npa_score
        score += npa_score

        # 2. Capital Impact Score (0-25)
        # Assuming unsecured for simplicity in MVP
        cap_score = 20.0 if lender_profile.lender_type == "public_sector_bank" else 15.0
        breakdown["capital_impact"] = cap_score
        score += cap_score

        # 3. Collateral Position Score (0-20)
        if not debt_profile.has_collateral:
            col_score = 20.0
            points.append("Unsecured debt: Bank has no physical asset to seize, maximizing your leverage.")
        else:
            col_score = -5.0
            points.append("Secured debt: Bank can invoke SARFAESI Act to auction the asset. Low leverage.")
        breakdown["collateral"] = col_score
        score += col_score

        # 4. Regulatory Protection Score (0-15)
        if debt_profile.debt_type == "education_loan":
            reg_score = 15.0
            points.append("Education Loan: Protected by specific RBI empathy directives. Leverage is high.")
        elif debt_profile.debt_type == "microfinance":
            reg_score = 12.0
            points.append("Microfinance: MFIN codes severely limit aggressive recovery tactics.")
        else:
            reg_score = 8.0
        breakdown["regulatory"] = reg_score
        score += reg_score

        # 5. Lender Motivation Score (0-10)
        # Example: Private banks known for high targets
        mot_score = 8.0 if lender_profile.lender_type == "private_sector_bank" else 10.0
        breakdown["lender_motivation"] = mot_score
        score += mot_score

        return LeverageAnalysis(
            leverage_score=max(0.0, min(100.0, score)),
            leverage_breakdown=breakdown,
            key_leverage_points=points
        )

    def calculate_settlement_range(
        self,
        debt_profile: DebtClassification,
        leverage: LeverageAnalysis,
        lender_profile: LenderProfile
    ) -> SettlementRange:
        """
        Estimates the settlement range.
        """
        base_outstanding = float(debt_profile.outstanding_amount)
        typical_min, typical_max = lender_profile.typical_settlement_range

        # If leverage is extremely high (>80), push below typical max
        if leverage.leverage_score >= 80:
            agg_pct = typical_min - 0.10
            real_pct = typical_min
            walk_pct = typical_max - 0.10
            rationale = "Your leverage is exceptionally high. Start with a very aggressive floor."
        else:
            agg_pct = typical_min
            real_pct = typical_max - 0.05
            walk_pct = typical_max + 0.10
            rationale = "Standard settlement bands apply based on crowd-sourced bank behavior."

        return SettlementRange(
            aggressive_ask=max(0.10, agg_pct) * base_outstanding,
            realistic_target=max(0.20, real_pct) * base_outstanding,
            walk_away_point=min(1.0, walk_pct) * base_outstanding,
            rationale=rationale
        )
