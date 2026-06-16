"""
Negotiation Strategy Pipeline (LangGraph).
Synthesizes the optimal negotiation strategy using RAG and Lender Intel.
"""
from typing import Dict, List
from loguru import logger
from ..models.cibil_engine import CIBILImpactEngine
from ..rag.lender_intel import LenderIntelDB
from ..rag.rbi_corpus import RBICorpusRAG

class NegotiationState:
    def __init__(self, profile: Dict):
        self.profile = profile
        self.lender_intel: Dict = {}
        self.rbi_citations: List[Dict] = []
        self.cibil_impact: Dict = {}
        self.final_strategy: Dict = {}

async def fetch_lender_intel_node(state: NegotiationState):
    db = LenderIntelDB()
    state.lender_intel = await db.get_settlement_range(
        state.profile["lender_name"],
        state.profile["loan_type"],
        state.profile["dpd"]
    )
    return state

async def run_cibil_engine_node(state: NegotiationState):
    engine = CIBILImpactEngine()
    
    target = "settlement" if state.profile["dpd"] >= 90 else "closure"
    state.cibil_impact = engine.calculate_impact(state.profile.get("cibil_score", 700), target)
    return state

async def fetch_rbi_rag_node(state: NegotiationState):
    rag = RBICorpusRAG()
    # E.g., user mentioned aggressive calling
    state.rbi_citations = await rag.retrieve_citations("harassment", state.profile["loan_type"])
    return state

def synthesize_strategy_node(state: NegotiationState):
    """
    Claude synthesizes the final 5-step playbook.
    """
    engine = CIBILImpactEngine()
    disclaimer = engine.get_disclaimer()
    
    # MOCK OUTPUT
    state.final_strategy = {
        "leverage": "High (70/100)",
        "target_settlement": f"Push for {state.lender_intel.get('avg_settlement_pct', 0) * 100}%",
        "red_flags": state.lender_intel.get("behavioral_note", ""),
        "cibil_warning": state.cibil_impact,
        "rbi_ammo": state.rbi_citations,
        "disclaimer": disclaimer
    }
    return state
