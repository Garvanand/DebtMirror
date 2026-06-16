"""
Formal Document Drafter.
Generates legal-grade counter-proposals, hardship letters, and Ombudsman escalations.
"""
from typing import Dict
from ..models.cibil_engine import CIBILImpactEngine

class DocumentDrafter:

    def draft_ots_proposal(self, profile: Dict, target_amount: float) -> str:
        """
        Drafts a One Time Settlement (OTS) proposal asserting the borrower's intent
        while establishing the upper limit of their capability.
        """
        engine = CIBILImpactEngine()
        disclaimer = engine.get_disclaimer()
        
        return f"""
        [Date]
        
        To,
        The Branch Manager / Recovery Dept,
        {profile['lender_name']}
        
        Subject: Request for One Time Settlement (OTS) for Loan/Card A/C No. XXXXXX
        
        Sir/Madam,
        
        Due to severe financial hardship, I have been unable to service my account.
        I am writing to propose a full and final One Time Settlement of Rs. {target_amount:,.2f} 
        against my outstanding dues.
        
        This amount represents my maximum borrowing capacity from family and friends. 
        If this is acceptable, please issue an official OTS letter stating that upon 
        payment, the account will be closed and the CIBIL status updated accordingly.
        
        I look forward to an amicable resolution.
        
        Sincerely,
        [Borrower Name]
        
        ---
        {disclaimer}
        """

    def draft_ombudsman_complaint(self, profile: Dict, harassment_logs: list) -> str:
        """
        Drafts a formal complaint to the RBI Banking Ombudsman invoking the 
        Fair Practices Code.
        """
        engine = CIBILImpactEngine()
        disclaimer = engine.get_disclaimer()
        
        return f"""
        [Date]
        To The Banking Ombudsman, RBI
        
        Subject: Complaint against {profile['lender_name']} for violation of Fair Practices Code.
        ...
        ---
        {disclaimer}
        """
