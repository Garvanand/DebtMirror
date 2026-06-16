"""
Debt Classification Engine.
Determines the legal framework and correct resolution pathway based on DPD and Loan Type.
"""
from pydantic import BaseModel
from typing import Literal, Optional, List
from enum import Enum
from decimal import Decimal

class DPDCategory(str, Enum):
    CURRENT = "current"             # 0-29 DPD
    SMA_0 = "sma_0"                # 30-59 DPD (Special Mention Account)
    SMA_1 = "sma_1"                # 60-89 DPD — CRITICAL WINDOW
    SMA_2 = "sma_2"                # 90+ DPD — approaching NPA
    SUB_STANDARD = "sub_standard"  # NPA < 12 months
    DOUBTFUL = "doubtful"          # NPA 12-36 months
    LOSS = "loss"                  # NPA > 36 months or written off

class NPAStatus(str, Enum):
    PERFORMING = "performing"
    SMA = "special_mention_account"
    NPA_SUB_STANDARD = "npa_sub_standard"
    NPA_DOUBTFUL = "npa_doubtful"
    NPA_LOSS = "npa_loss"
    WRITTEN_OFF = "written_off"     # bank has taken P&L hit
    SOLD_TO_ARC = "sold_to_arc"     # transferred to Asset Reconstruction Company

class ResolutionPathway(str, Enum):
    EMI_RESTRUCTURING = "emi_restructuring"  # extend tenure, reduce EMI
    MORATORIUM = "moratorium"                # temporary payment pause
    OTS_NEGOTIATION = "ots"                  # One Time Settlement
    DRS = "debt_restructuring_scheme"        # formal restructuring
    IBC_RESOLUTION = "ibc"                   # for large debts
    OMBUDSMAN_ESCALATION = "ombudsman"       # when bank is uncooperative
    LEGAL_DEFENCE = "legal_defence"          # when bank initiates legal action

class DebtClassification(BaseModel):
    debt_type: Literal[
        "credit_card", "personal_loan", "education_loan",
        "home_loan", "auto_loan", "msme_loan", "microfinance",
        "buy_now_pay_later", "salary_advance"
    ]
    lender_type: Literal[
        "public_sector_bank", "private_sector_bank", "nbfc",
        "cooperative_bank", "microfinance_institution",
        "digital_lender", "credit_card_company"
    ]
    outstanding_amount: Decimal
    original_amount: Decimal
    months_overdue: int             # DPD ÷ 30
    dpd_category: DPDCategory
    npa_status: NPAStatus
    has_collateral: bool            # secured vs unsecured
    collateral_type: Optional[str]
    applicable_frameworks: List[str]  # which laws/regulations apply
    recommended_pathway: ResolutionPathway
    pathway_rationale: str
