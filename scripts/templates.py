"""
Written Communication Templates.
Generates the legal-grade documents required to force formal lender action.
"""

class FormalDocumentTemplates:

    HARDSHIP_LETTER_PROMPT = """
Draft a formal Hardship Letter (Restructuring Request).
Format: Plain paper, delivered via registered post + email.
Must include:
- Formal opening: "The Branch Manager, [Bank Name], [Branch Address]"
- Subject: "Request for Loan Restructuring under RBI Master Circular..."
- Account details
- Detailed hardship narrative (factual, specific, no emotion)
- Current income/expenses (honest representation)
- Proposed resolution (EMI amount borrower CAN pay)
- Request for meeting
- Regulatory basis for request
- Non-negotiable Disclaimer
"""

    OTS_COUNTER_PROPOSAL_PROMPT = """
Draft a formal One Time Settlement (OTS) Counter-Proposal Letter.
This is the most powerful letter. It MUST include:
- Reference to lender's initial offer (with date)
- Borrower's specific counter offer amount: {counter_offer_amount}
- Breakdown of how the borrower arrived at this amount
- Timeline the borrower can commit to (e.g., lump sum within 15 days)
- CONDITION: "Upon agreement, request confirmation that account will be marked 'Settled' in CIBIL and not 'Written Off'"
- RBI circular citation supporting OTS eligibility
- Deadline for response
- Non-negotiable Disclaimer
"""

    ESCALATION_LETTER_PROMPT = """
Draft an Escalation Letter to the Head/Zonal Office.
Used when the branch is unresponsive or acting in bad faith.
Must include:
- Timeline of attempts (dates, person spoken to, outcome)
- Regulatory obligation to respond (cite Fair Practices Code)
- What resolution is being sought
- Formal Notice: "If no response is received within 15 days, I will escalate this grievance to the RBI Banking Ombudsman."
- Non-negotiable Disclaimer
"""

    OMBUDSMAN_COMPLAINT_PROMPT = """
Draft an RBI Banking Ombudsman Complaint Evidence Package.
This is handed off to RiteOfWay (Day 06) for formal filing.
Must include:
- Executive Summary of the grievance
- Timeline of all communications
- Evidence of restructuring requests (sent letters, emails)
- Lender's responses (or lack thereof)
- Specific RBI provisions the lender is violating (e.g., Harassment clauses, failure to acknowledge restructuring)
- Specific relief requested by the borrower
- Non-negotiable Disclaimer
"""
