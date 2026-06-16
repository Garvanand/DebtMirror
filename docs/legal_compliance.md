# DebtMirror: Legal Compliance & Risk Mitigation

DebtMirror operates in a high-risk domain. Giving incorrect financial advice can permanently damage a user's credit profile or expose them to legal jeopardy. This document outlines the absolute, zero-tolerance compliance constraints engineered into the system.

## 1. The Non-Negotiable Legal Disclaimer

DebtMirror is a **negotiation intelligence tool, NOT a legal advisor.**

### Implementation Rule
Every single user-facing output—whether a WhatsApp script, a Hardship Letter, or an OTS Proposal—**MUST** be appended with the following text:

> *"⚠️ This is informational guidance based on publicly available RBI regulations. For complex debt matters, consult a qualified advocate or CIBIL-certified credit counselor."*

### Enforcement
This is strictly enforced at the Evaluation Harness level (`eval/harness.py`). Any generated script lacking this disclaimer instantly fails the build pipeline under Category D (Zero Tolerance).

## 2. Prohibition on Fraudulent Advice

DebtMirror operates under a strict ethical constraint. The LLM prompts explicitly forbid generating scripts or strategies that include:
- Advising the borrower to "strategically default" (intentionally stopping payment to force a settlement).
- Advising the borrower to hide assets or transfer funds to avoid recovery.
- Providing false or fabricated reasons for financial hardship.

## 3. RBI Regulatory RAG (Hallucination Prevention)

To prevent the LLM from hallucinating fake laws (e.g., "Under RBI Code 99, you don't have to pay"), DebtMirror exclusively relies on a ChromaDB RAG filled with specific, verified documents.

### Indexed Documents:
1. **Prudential Norms on Income Recognition, Asset Classification and Provisioning** (The definitive rulebook on NPA provisioning).
2. **Fair Practices Code for NBFCs** (Governs recovery agent behavior).
3. **Banking Ombudsman Scheme 2006** (Defines escalation pathways).
4. **Master Direction on Interest Rate on Deposits and Advances** (Dictates penal interest capitalization).

If a query requires a citation, the system extracts the exact text from the ChromaDB chunk and generates a standardized legal citation (e.g., *RBI Master Circular No. RBI/2023-24/09, Section 4.2.3*).

## 4. Explicit CIBIL Modeling

Debt settlement is a double-edged sword. DebtMirror enforces full transparency regarding credit impact.

The system will never advise a settlement without forcing the user to acknowledge the consequences via the `models/cibil_engine.py`:
- **Closure**: 0 to -20 points (Recoverable in 6-12 months).
- **Settlement (OTS)**: -50 to -100 points (Stays on report for 7 years).
- **Written Off**: -200 points (Stays on report for 7+ years).

By mathematically modeling these paths, the system protects the borrower from making decisions based solely on immediate cash flow relief at the expense of long-term financial health.
