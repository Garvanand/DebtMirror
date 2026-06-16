"""
CIBIL Dispute Advisor.
Analyzes credit reports for actionable errors and generates formal dispute letters.
"""
from pydantic import BaseModel
from typing import List, Optional
from loguru import logger

class CIBILEntry(BaseModel):
    account_number: str
    lender_name: str
    reported_dpd: int
    reported_status: str
    outstanding_balance: float

class DisputeAnalysis(BaseModel):
    is_valid_dispute: bool
    dispute_ground: str
    success_probability: str
    required_evidence: List[str]
    escalation_path: str

class DisputeDetails(BaseModel):
    member_reference_number: str
    account_number: str
    lender_name: str
    dispute_reason: str
    evidence_description: str

class CIBILDisputeAdvisor:

    async def analyze_dispute_eligibility(
        self,
        cibil_entry: CIBILEntry,
        borrower_evidence: List[str]
    ) -> DisputeAnalysis:
        """
        Evaluates if the borrower has a legitimate ground to dispute a CIBIL entry.
        """
        logger.info(f"Analyzing dispute for account {cibil_entry.account_number}")
        
        # MOCK Logic
        if cibil_entry.reported_status == "Written Off" and "ots_clearance_letter" in borrower_evidence:
            return DisputeAnalysis(
                is_valid_dispute=True,
                dispute_ground="Account marked as Written Off after successful OTS settlement.",
                success_probability="High - Supported by RBI mandates",
                required_evidence=["OTS Settlement Letter", "Bank Statement showing final payment"],
                escalation_path="CIBIL Dispute -> Banking Ombudsman"
            )
            
        return DisputeAnalysis(
            is_valid_dispute=False,
            dispute_ground="None detected.",
            success_probability="Low",
            required_evidence=[],
            escalation_path="N/A"
        )

    def generate_cibil_dispute_letter(self, dispute: DisputeDetails) -> str:
        """
        Generates the strict format required by CIBIL's dispute resolution matrix.
        """
        return f"""
        To,
        Consumer Disputes Division,
        TransUnion CIBIL Limited
        Email: consumer.disputes@cibil.com
        
        Subject: Dispute regarding incorrect entry for Account No. {dispute.account_number}
        
        Sir/Madam,
        
        I am writing to formally dispute an inaccurate entry on my CIBIL report.
        
        Member Reference Number: {dispute.member_reference_number}
        Lender Name: {dispute.lender_name}
        Account Number: {dispute.account_number}
        
        Reason for Dispute:
        {dispute.dispute_reason}
        
        I have attached the following evidence supporting my claim:
        {dispute.evidence_description}
        
        As per RBI directives on Credit Information Companies, I request you to investigate 
        this matter with the lender and rectify my credit report within 30 days.
        
        If this is not resolved, I will be forced to escalate the matter to the RBI Ombudsman.
        
        Sincerely,
        [Borrower Name]
        
        ---
        ⚠️ This is informational guidance based on publicly available RBI regulations. 
        For complex debt matters, consult a qualified advocate or CIBIL-certified credit counselor.
        """
