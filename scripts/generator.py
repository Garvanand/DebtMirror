"""
Script Generation Logic.
Generates highly tailored Stage 1 and Stage 2 negotiation scripts for borrowers.
"""
from loguru import logger
from typing import Dict, Any

class ScriptGenerator:

    STAGE_1_SYSTEM_PROMPT = """
You are DebtMirror, an elite debt negotiation intelligence engine.
Generate a Stage 1 (Opening) phone call script for a borrower contacting their lender.

OBJECTIVE: Establish hardship, request a restructuring/OTS discussion, and signal that the borrower knows their RBI rights.
DO NOT INCLUDE: Groveling, unachievable promises, or revealing maximum capacity.

The script MUST generate the following exact sections matching the `NegotiationScript` schema:

1. OPENING STATEMENT (Read verbatim or adapt):
"Namaste / Hello, I am calling regarding my [loan_type] account number [XXXX]. My name is [name]. I have been facing genuine financial hardship due to [hardship_reason]. I am calling today to discuss restructuring options available under RBI guidelines before my account classification changes."

2. KEY POINTS TO COVER (Strict Order):
- Acknowledge the overdue (do not deny).
- State the genuine hardship specifically.
- Express intent to resolve.
- Request specific restructuring/OTS information under the RBI Master Circular.
- Do NOT reveal maximum repayment capacity.
- Ask for next meeting / written communication.

3. REGULATORY CITATIONS:
Inject the specific citations provided in your context (e.g., RBI Master Circular on Customer Service, Fair Practices Code).

4. RESPONSES TO COMMON TACTICS:
- If "You must pay the full amount": "I understand, however I am requesting information about the OTS policy as permitted under RBI Fair Practices Code."
- If "We'll send you to collections": "I am communicating in good faith to resolve this. May I have your name and employee ID for our records?"
- If "You'll lose your CIBIL score anyway": "I am aware of the CIBIL implications and am trying to resolve this within the framework that works for both parties."

Context Data:
Profile: {profile}
Citations: {citations}
"""

    async def generate_counter_script(
        self,
        case: Dict,
        lender_initial_offer: float,
        settlement_range: Dict
    ) -> Dict:
        """
        Stage 2 Logic: After lender makes an initial offer.
        """
        logger.info(f"Generating Stage 2 counter-script against offer: {lender_initial_offer}")
        
        target = settlement_range["realistic_target"]
        walk_away = settlement_range["walk_away_point"]
        
        # Determine strategic stance
        if lender_initial_offer <= target:
            stance = "accept_with_conditions"
            action = "Accept the offer conditional on receiving a No Dues Certificate (NDC) stating 'Settled' rather than 'Written Off'."
        elif target < lender_initial_offer <= walk_away:
            stance = "midpoint_counter"
            action = f"Counter at {(lender_initial_offer + target) / 2:,.0f}. Acknowledge offer respectfully, reference financial capacity limits."
        else:
            stance = "reject_and_escalate"
            action = "Reject the offer as it exceeds financial capacity. Escalate to Zonal Office."
            
        return {
            "stage": "counter",
            "stance_taken": stance,
            "strategic_action": action,
            "responses_to_common_tactics": {
                "This is a final offer": "Thank you for the offer. Unfortunately, it exceeds my documented hardship capacity. I will need to escalate this to the Zonal grievance officer for further review."
            }
        }
