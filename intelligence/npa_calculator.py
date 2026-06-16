"""
NPA Timeline & Capital Impact Calculator.
Quantifies exactly how much money the bank loses in provisions if the loan defaults.
"""
from decimal import Decimal
from typing import Dict

class BankImpactAnalysis(Dict):
    pass

class NPATimelineCalculator:

    def calculate_bank_impact(
        self,
        outstanding: Decimal,
        dpd: int,
        lender_type: str
    ) -> BankImpactAnalysis:
        """
        Calculates the provisioning burden for the bank under RBI Prudential Norms.
        """
        required_provision_pct = Decimal('0.0')
        npa_status_display = "Performing / SMA"

        # SMA accounts: 0% provisioning (Standard Asset)
        if dpd < 90:
            required_provision_pct = Decimal('0.0')
        # Sub-standard NPA (< 12 months NPA): 15% provisioning
        elif 90 <= dpd < 450:
            required_provision_pct = Decimal('0.15')
            npa_status_display = "Sub-Standard NPA"
        # Doubtful NPA (12-36 months): 25-100%
        elif 450 <= dpd < 1170:
            required_provision_pct = Decimal('0.40') # Averaged for Doubtful
            npa_status_display = "Doubtful NPA"
        # Loss NPA: 100%
        else:
            required_provision_pct = Decimal('1.0')
            npa_status_display = "Loss Asset"

        provisioning_burden = outstanding * required_provision_pct

        return BankImpactAnalysis({
            "current_npa_status": npa_status_display,
            "required_provision_pct": float(required_provision_pct),
            "provisioning_burden_amount": float(provisioning_burden),
            "bank_motivation_level": "High" if required_provision_pct > 0 else "Moderate"
        })
