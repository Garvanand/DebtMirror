"""
DebtMirror WhatsApp Handler.
Conversational orchestrator for Multi-lingual Debt Negotiation Intelligence.
"""
from typing import Dict, Any, Optional
from loguru import logger
import json

class WhatsAppSessionState:
    """Mock Redis Session Wrapper"""
    def __init__(self):
        self._state = {}

    def get_state(self, user_phone: str) -> Dict:
        return self._state.get(user_phone, {"stage": "init", "case_data": {}})

    def update_state(self, user_phone: str, updates: Dict):
        current = self.get_state(user_phone)
        current.update(updates)
        self._state[user_phone] = current

class DebtMirrorWhatsApp:

    def __init__(self):
        self.session_db = WhatsAppSessionState()

    async def handle_incoming_message(self, user_phone: str, message: str, language: str = "hi") -> str:
        """
        Main entry point for incoming WhatsApp messages.
        """
        logger.info(f"Incoming from {user_phone}: {message}")
        
        state = self.session_db.get_state(user_phone)
        msg_lower = message.lower()

        # 1. DEBT INTAKE FLOW
        if "overdue" in msg_lower or "outstanding" in msg_lower:
            return await self._handle_intake(user_phone, message)

        # 2. SCRIPT REQUEST FLOW
        elif "script" in msg_lower or "call karna" in msg_lower:
            return await self._handle_script_request(user_phone, state)

        # 3. OFFER EVALUATION FLOW
        elif "settle karne" in msg_lower or "offer" in msg_lower:
            return await self._handle_offer_evaluation(user_phone, message, state)

        # 4. DOCUMENT REQUEST FLOW
        elif "hardship letter" in msg_lower or "write a" in msg_lower:
            return await self._handle_document_request(user_phone, state)

        # 5. CIBIL QUERY FLOW
        elif "cibil" in msg_lower:
            return await self._handle_cibil_query(user_phone)

        # Continue Intake Questions
        if state["stage"] == "intake_questions":
            self.session_db.update_state(user_phone, {"stage": "intake_complete", "case_data": {"dpd": 120, "lender": "SBI", "loan_type": "personal_loan"}})
            return "Theek hai. Yeh main aapke liye calculate kar raha hun...\n\n(Generating leverage analysis... Your leverage is HIGH due to 120 DPD on an unsecured loan. The bank is motivated to settle.)"

        return "Main DebtMirror hun. Aap apne loan, CIBIL, ya bank calls ke baare mein sawaal pooch sakte hain."

    async def _handle_intake(self, user_phone: str, message: str) -> str:
        self.session_db.update_state(user_phone, {"stage": "intake_questions"})
        return (
            "Samjha. Kuch quick sawaal:\n"
            "1. Loan kitne saal pehle liya tha?\n"
            "2. Abhi koi EMI dena possible hai ya bilkul nahi?\n"
            "3. Collateral hai? (home/car/FD)"
        )

    async def _handle_script_request(self, user_phone: str, state: Dict) -> str:
        if state.get("stage") == "intake_complete":
            return (
                "STAGE 1 OPENING SCRIPT (Call read-out):\n\n"
                "Namaste, main [Aapka Naam] bol raha hun loan account [XXXX] ke baare mein. "
                "Main financial hardship face kar raha hun [Reason] ki wajah se. "
                "Main apne account ka RBI Master Circular ke tahat restructuring options discuss karna chahta hun.\n\n"
                "⚠️ DO NOT SAY: 'Mere paas paise nahi hain'. \n"
                "SAY: 'Main resolve karna chahta hun, restructure options bataiye.'"
            )
        return "Pehle mujhe aapke loan ki details bataiye taaki main correct script bana sakun."

    async def _handle_offer_evaluation(self, user_phone: str, message: str, state: Dict) -> str:
        # MOCK calculation: Bank offered 2.2L on 3.2L outstanding (68.75%)
        return (
            "Bank ne 68.75% par settlement offer kiya hai.\n"
            "Hamara data dikhata hai ki SBI 4 months DPD (SMA-2) par typically 50-60% par settle karta hai.\n"
            "👉 REJECT this offer. Counter at ₹1.9L (59%). Yeh branch manager ke authority level mein hai."
        )

    async def _handle_document_request(self, user_phone: str, state: Dict) -> str:
        # MOCK Hardship Letter Generation
        return (
            "📄 Aapka Formal Hardship Letter generate ho gaya hai (English mein, bank ke liye).\n"
            "Ise Registered Post aur Email dono se bhejein.\n\n"
            "[Link to PDF: https://debtmirror.agentos/docs/hardship_123.pdf]\n\n"
            "Disclaimer: This is informational guidance based on RBI regulations."
        )

    async def _handle_cibil_query(self, user_phone: str) -> str:
        return (
            "Settlement karne se aapka status 'Settled' dikhega aur score approx 100 points girega.\n"
            "Lekin, agar aap kuch nahi karte, toh 'Written Off' mark hoga jo 200+ points girayega aur sabse zyada damaging hai.\n"
            "👉 'Settled' status 7 saal tak rehta hai, par score 3 saal mein recover ho sakta hai naye credit card (FD backed) se."
        )
