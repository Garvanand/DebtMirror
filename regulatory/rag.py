"""
Regulatory RAG Engine.
Provides citation-backed defense mechanisms for borrowers against predatory claims.
"""
from typing import List
from loguru import logger
from .schemas import RegulatoryProvision, BorrowerRight, ValidationResult
from ..intelligence.classification import DebtClassification

class RegulatoryRAG:

    async def find_applicable_provisions(
        self,
        query: str,
        debt_type: str,
        negotiation_stage: str
    ) -> List[RegulatoryProvision]:
        """
        Queries ChromaDB for specific regulatory provisions to use as leverage.
        """
        logger.info(f"Querying RAG for: '{query}' | context: {debt_type}, {negotiation_stage}")
        
        # MOCK ChromaDB Retrieval
        if "interest" in query.lower() or "penal" in query.lower():
            return [
                RegulatoryProvision(
                    citation_format="RBI Guidelines on Fair Practices Code, Circular DBR.No.Dir.BC.10/13.03.00/2015-16",
                    plain_english_summary="Banks cannot capitalize penal interest. It must be charged separately and not added to the principal.",
                    borrower_benefit="You can demand a revised statement separating penal interest, immediately lowering your compound interest burden."
                )
            ]
        return []

    async def get_borrower_rights(
        self,
        debt_classification: DebtClassification
    ) -> List[BorrowerRight]:
        """
        Determines exactly what rights this borrower has right now.
        """
        logger.info(f"Retrieving standard rights for {debt_classification.debt_type} at {debt_classification.dpd_category}")
        rights = [
            BorrowerRight(
                category="Collection Hours",
                description="Recovery agents cannot contact you before 0700 hours or after 1900 hours.",
                citation_format="RBI Master Circular on Customer Service in Banks, Section 4.2.3"
            )
        ]
        
        if debt_classification.debt_type == "education_loan":
            rights.append(
                BorrowerRight(
                    category="Moratorium Rights",
                    description="Banks must provide a moratorium extending up to 6 months after getting a job, or 1 year after course completion, whichever is earlier.",
                    citation_format="IBA Model Educational Loan Scheme"
                )
            )
        return rights

    async def validate_lender_claim(
        self,
        lender_claim: str,
        debt_type: str
    ) -> ValidationResult:
        """
        The truth-detector. Validates if what the bank's recovery agent is saying is legally true.
        """
        logger.info(f"Validating lender claim: '{lender_claim}'")
        
        # MOCK Validation Logic (Would use LLM + RAG to assess the claim)
        if "pay all penalties before" in lender_claim.lower() or "settlement" in lender_claim.lower():
            return ValidationResult(
                is_claim_valid=False,
                explanation="The bank is attempting to artificially inflate the baseline before negotiating a settlement. There is no legal mandate that penalties must be cleared to initiate an OTS.",
                refuting_citation="RBI Master Circular - Prudential Norms (Compromise Settlements)"
            )
            
        return ValidationResult(
            is_claim_valid=True,
            explanation="The claim aligns with standard recovery procedures.",
            refuting_citation=None
        )
