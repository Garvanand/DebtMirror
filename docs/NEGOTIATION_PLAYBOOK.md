# DebtMirror: Negotiation Playbook & Leverage Engine

DebtMirror turns terrified borrowers into informed negotiators. This document explains how the Leverage Engine works and how the conversational scripts are dynamically generated.

## 1. The Mathematical Leverage Engine

Before generating a script, DebtMirror calculates the borrower's "Leverage Score" out of 100 based on five variables:

1. **NPA Pressure**: The "Golden Window" is between 60 and 89 DPD (SMA-1). Here, the bank is highly motivated to settle because at 90 DPD, the loan becomes an NPA and the bank must take a 15% hit to their balance sheet provisioning. DebtMirror exposes this hidden urgency.
2. **Capital Impact**: Public Sector Banks (PSBs) are heavily penalized for NPAs hitting their Tier-1 capital ratios, making them more pliable.
3. **Collateral**: Unsecured debt (e.g., Credit Cards, Personal Loans) provides the borrower massive leverage, as the bank has no physical asset to seize.
4. **Regulatory Shield**: Specific loans (like Education or MSME loans) have RBI protections that prevent aggressive recovery.
5. **Lender Tactics**: Internal crowd-sourced data dictates how aggressive a specific lender is (e.g., *HDFC typically starts settlement offers low, but zones out higher*).

## 2. Dynamic Script Generation

DebtMirror operates in three distinct negotiation stages.

### Stage 1: The Opening Contact
The goal of Stage 1 is to establish hardship without giving up leverage.
- **What it does**: Generates a verbatim phone script acknowledging the debt, stating the genuine hardship, and requesting restructuring options under the RBI Master Circular.
- **What it prevents**: The script explicitly warns the borrower **NOT** to reveal their maximum repayment capacity or make promises they can't keep.

### Stage 2: The Counter-Offer
When the bank makes an initial offer, DebtMirror evaluates it against the mathematical `SettlementRange`.
- If the offer is above the realistic target, DebtMirror advises acceptance with the strict condition of an NDC (No Dues Certificate) marked "Settled".
- If the offer is poor, DebtMirror generates a counter-offer script, lowering the floor and referencing the borrower's documented financial capacity.

### Stage 3: Escalation
If the branch manager is hostile or refuses to engage:
- DebtMirror auto-generates a formal Escalation Letter to the Zonal Office, citing the RBI Fair Practices Code's mandate that banks must respond to restructuring requests.
- If the Zonal Office fails, DebtMirror prepares the evidence package for an RBI Banking Ombudsman complaint (handed off to the RiteOfWay agent).
