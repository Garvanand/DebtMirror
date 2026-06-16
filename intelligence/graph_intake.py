"""
Intake Pipeline (LangGraph).
Extracts structured data from natural language and calculates borrower leverage.
"""
from typing import Dict, Any
from loguru import logger
from ..models.schemas import DebtProfile

class IntakeState:
    def __init__(self, raw_message: str):
        self.raw_message = raw_message
        self.extracted_profile: Dict = {}
        self.leverage_score: float = 0.0
        self.optimal_path: str = ""

def extract_profile_node(state: IntakeState):
    """Uses Groq LLaMA to pull debt variables from WhatsApp message."""
    logger.info("Extracting debt variables from user message...")
    # MOCK EXTRACT
    state.extracted_profile = {
        "lender_name": "HDFC",
        "loan_type": "credit_card",
        "outstanding_amount": 150000,
        "dpd": 110,
        "cibil_score": 580
    }
    return state

def calculate_leverage_node(state: IntakeState):
    """
    Mathematical leverage calculation.
    Information Asymmetry Breaker: Leverage peaks right around 90 DPD (NPA classification).
    """
    logger.info("Calculating borrower leverage...")
    
    dpd = state.extracted_profile["dpd"]
    loan_type = state.extracted_profile["loan_type"]
    
    score = 50.0
    
    # 1. Secured vs Unsecured
    if loan_type in ["home_loan", "auto_loan"]:
        score -= 30.0 # Asset-backed. Low borrower leverage.
    else:
        score += 20.0 # Unsecured. High borrower leverage.
        
    # 2. DPD Leverage Curve
    if dpd < 30:
        score -= 20.0 # Bank has no incentive
    elif 60 <= dpd <= 89:
        score += 30.0 # Golden window. Bank desperate to avoid NPA provisioning
    elif dpd >= 180:
        score += 15.0 # Debt is old. Recovery chances low. Bank willing to write off.

    state.leverage_score = max(0.0, min(100.0, score))
    return state

def classify_path_node(state: IntakeState):
    """Decision Tree mapping."""
    dpd = state.extracted_profile["dpd"]
    loan_type = state.extracted_profile["loan_type"]
    
    if loan_type == "home_loan":
        state.optimal_path = "emi_restructuring"
    elif dpd < 60:
        state.optimal_path = "hardship_waiver"
    else:
        state.optimal_path = "ots_settlement" # One Time Settlement
        
    return state
