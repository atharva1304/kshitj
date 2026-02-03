# Agentic Honeypot API

## Overview

A FastAPI backend that detects scam messages and extracts scam intelligence (UPI IDs, bank accounts, phishing links, phone numbers). Designed for automated evaluation and integration.

---

## Endpoint

| Method | Path |
|--------|------|
| `POST` | `/api/honeypot/analyze` |

---

## Authentication

All requests require an API key via the `x-api-key` header.

| Header | Required |
|--------|----------|
| `x-api-key` | Yes |

Requests without a valid API key return `401 Unauthorized`.

---

## Request Format

```json
{
  "message": "string (required)",
  "conversation_id": "string (optional)"
}
```

**Example:**
```json
{
  "message": "Send money to UPI ID scammer@upi immediately!",
  "conversation_id": "conv-123"
}
```

---

## Response Format

### Non-Scam Response

When no scam indicators are detected:

```json
{
  "scam_detected": false,
  "confidence": 0.1,
  "scam_type": null,
  "extracted_intelligence": null,
  "risk_score": null,
  "agent_metadata": null,
  "message": "No scam indicators detected",
  "status": "success"
}
```

### Scam-Detected Response

When scam indicators are found:

```json
{
  "scam_detected": true,
  "confidence": 0.95,
  "scam_type": "generic_scam",
  "extracted_intelligence": {
    "upi_ids": ["scammer@upi"],
    "bank_accounts": [],
    "ifsc_codes": [],
    "phishing_links": [],
    "phone_numbers": []
  },
  "risk_score": 3.0,
  "agent_metadata": {
    "persona_used": "elderly_user",
    "conversation_strategy": "trust_then_verify"
  },
  "message": null,
  "status": "success"
}
```

---

## Error Responses

All errors return JSON in this format:

```json
{
  "status": "error",
  "message": "<human readable message>"
}
```

| Status Code | Description |
|-------------|-------------|
| `401` | Missing or invalid API key |
| `400` | Invalid or missing request body |
| `500` | Internal server error |

---

## Stability Guarantees

- **Always returns JSON** — No HTML error pages
- **Never crashes on invalid input** — Empty, whitespace-only, or very long messages are handled gracefully
- **Safe for automated evaluation** — Deterministic behavior for all inputs

---

## Notes for Evaluators

- **PowerShell display quirk:** Arrays may display as `System.Object[]` in terminal output, but the actual HTTP response is valid JSON. Use `| ConvertTo-Json` or test with tools like `curl` or Postman for accurate output.

- **Test with curl:**
  ```bash
  curl -X POST "http://localhost:8000/api/honeypot/analyze" \
    -H "Content-Type: application/json" \
    -H "x-api-key: test-key" \
    -d '{"message": "Send money to UPI scammer@upi now!"}'
  ```

---

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

Default API key for local testing: `test-key` (set via `API_KEY` environment variable).
