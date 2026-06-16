# DebtMirror: CIBIL Impact & Recovery Guide

Understanding CIBIL (Credit Information Bureau (India) Limited) impact is critical. Most borrowers are paralyzed by the fear of ruining their credit score, preventing them from making logical settlement decisions. DebtMirror breaks this asymmetry by explicitly mapping out the credit consequences of every action.

## 1. Credit Status Outcomes

DebtMirror models five specific resolution paths and their credit score impacts. 

| Resolution Path | Resulting CIBIL Status | Immediate Score Drop | Recovery Timeline |
|-----------------|------------------------|----------------------|-------------------|
| **Full Payment** | Closed | 0 points | N/A |
| **EMI Restructuring** | Restructured | ~50 points | 24 months |
| **OTS Settlement** | Settled | ~100 points | 36 months |
| **Default (NPA)** | Sub-Standard | ~150 points | 48 months |
| **Total Default** | Written Off | 200+ points | 60+ months |

**Key Takeaway**: DebtMirror forces the user to see that an OTS Settlement (`-100` points) is mathematically superior to ignoring the debt and letting it hit Written Off (`-200` points).

## 2. CIBIL Dispute Management

Lenders frequently report inaccurate data post-settlement. DebtMirror actively assists borrowers in challenging these entries.

**Common Legitimate Dispute Grounds:**
1. **Wrong Outstanding Amount**: The balance doesn't reflect the recent settlement.
2. **Account Marked "Written Off" instead of "Settled"**: Banks are legally required to update the status to "Settled" within 30 days of an OTS clearance. If they fail, DebtMirror flags it.
3. **Incorrect DPD**: The loan was current when marked overdue.

When DebtMirror detects an actionable error, it generates a strict, formalized CIBIL Dispute Letter formatted specifically for `consumer.disputes@cibil.com`, complete with references to RBI Credit Information Company directives.

## 3. The 36-Month Recovery Roadmap

If a borrower executes a settlement, DebtMirror generates a month-by-month recovery plan to restore their score to 750+.

- **Months 1-6 (Stabilization)**: The score stops dropping because DPD stops accumulating. The primary objective here is to secure the OTS clearance letter and verify CIBIL reflects "Settled".
- **Months 6-18 (Gradual Recovery)**: Positive existing accounts carry more weight. DebtMirror advises opening a Secured Credit Card (FD-backed) to rebuild a positive repayment history.
- **Months 18-36 (Normalization)**: The negative weight of the "Settled" status diminishes significantly. By keeping credit utilization < 30% and never missing a new EMI, full recovery is achievable.
