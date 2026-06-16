# DebtMirror: API Documentation

This document outlines the internal and cross-agent APIs exposed by DebtMirror. These APIs are used by the WhatsApp integration layer and the AgentOS inter-agent mesh.

## Base URL
All internal requests should be routed to the FastAPI instance at `http://debtmirror_api:8010`.

---

## 1. AgentOS Mesh Integration APIs

### `POST /v1/agentOS/debt/intake`
Triggered proactively by GhostCFO or directly by user input to initiate a debt case.

**Request Body:**
```json
{
  "user_id": "string",
  "debt_description": "string",
  "triggered_by_agent": "string"
}
```

**Response:**
```json
{
  "case_id": "string",
  "initial_briefing": "string",
  "leverage_score": "float"
}
```

### `GET /v1/agentOS/debt/context/{user_id}`
Retrieves the high-level debt stress context for a given user. Shared across AgentOS.

**Response:**
```json
{
  "debt_stress_active": true,
  "highest_dpd": 120,
  "legal_action_risk": "low"
}
```

### `POST /v1/agentOS/debt/escalate_to_ombudsman`
Routes a failed negotiation package directly to RiteOfWay (Day 06) for formal grievance filing.

**Request Body:**
```json
{
  "case_id": "string",
  "reason": "string",
  "communications_log": ["string"]
}
```

**Response:**
```json
{
  "status": "escalated_to_riteofway",
  "evidence": {
    "case_summary": "string",
    "regulatory_violations": ["string"]
  }
}
```

---

## 2. Intelligence APIs (Internal)

### `POST /v1/debtmirror/integrations/ghostcfo/stress_trigger`
Dedicated endpoint specifically tuned for GhostCFO's runway logic.

**Request Body:**
```json
{
  "user_id": "string",
  "lender_name": "string",
  "runway_days": 30,
  "monthly_emi": 45000.0
}
```

### `GET /v1/debtmirror/integrations/glassroom/coaching/{case_id}`
Polled continuously by GlassRoom during a live borrower-lender call to fetch real-time rebuttal scripts.

**Response:**
```json
{
  "rebuttal": "Do not commit to paying tomorrow. State you need 7 days to review."
}
```

---

## 3. Webhook: WhatsApp Server

While WhatsApp handles conversational routing internally, it interfaces with the state machine. The primary handler logic resides in `server/whatsapp_handler.py`.

*Note: In production, the WhatsApp webhook would listen on `POST /v1/webhooks/whatsapp` and parse the incoming Twilio/Meta payload.*
