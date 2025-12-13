# Model-to-Grid API Endpoints

## Firmus AI Cloud Discount Qualification API Documentation

This document describes the REST API endpoints for the Model-to-Grid pricing program, which allows developers to qualify models for energy-based pricing discounts.

---

## Base URL

```
https://api.firmus.ai/v1
```

## Authentication

All endpoints require Bearer token authentication:

```bash
Authorization: Bearer <your_firmus_api_token>
```

Get your API token from the [Firmus Dashboard](https://dashboard.firmus.ai/settings/api-keys).

---

## Endpoints

### 1. Submit Model for Qualification

Submit a model for Model-to-Grid discount qualification.

**Endpoint:** `POST /model-to-grid/qualify`

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "model_id": "my-llama-70b-v1",
  "model_name": "Custom Llama 70B Optimized",
  "architecture": "llama-3",
  "parameter_count": "70B",
  "quantization": "FP16",
  "framework": "PyTorch",
  "declared_metrics": {
    "avg_power_watts": 145.2,
    "peak_power_watts": 162.8,
    "power_cv": 0.092,
    "joules_per_token": 2.8,
    "tokens_per_joule": 0.357
  },
  "test_environment": {
    "hardware": "H200 80GB HBM3",
    "driver_version": "550.54.15",
    "cuda_version": "12.4",
    "test_duration_minutes": 15,
    "num_samples": 50,
    "batch_size": 1,
    "sequence_length": 512
  },
  "model_card_url": "https://github.com/myorg/mymodel/MODEL_CARD.md",
  "contact_email": "dev@myorg.com"
}
```

**Response (202 Accepted):**
```json
{
  "status": "qualification_pending",
  "qualification_id": "qual_7x9k2m4p8n1",
  "model_id": "my-llama-70b-v1",
  "submitted_at": "2025-12-13T22:30:00Z",
  "estimated_completion": "2025-12-15T10:00:00Z",
  "message": "Model submitted for qualification. Verification will complete within 24-48 hours.",
  "next_steps": {
    "check_status": "/model-to-grid/qualify/qual_7x9k2m4p8n1",
    "webhook_url": "https://api.firmus.ai/v1/webhooks/model-qualification"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Missing or invalid API token
- `429 Too Many Requests` - Rate limit exceeded (max 10 submissions/day)

---

### 2. Check Qualification Status

Retrieve the current status of a model qualification request.

**Endpoint:** `GET /model-to-grid/qualify/{qualification_id}`

**Request Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK - Pending):**
```json
{
  "status": "verification_in_progress",
  "qualification_id": "qual_7x9k2m4p8n1",
  "model_id": "my-llama-70b-v1",
  "submitted_at": "2025-12-13T22:30:00Z",
  "progress": {
    "stage": "micro_benchmark_profiling",
    "percent_complete": 60,
    "current_step": "Running power stability tests",
    "estimated_completion": "2025-12-14T08:15:00Z"
  }
}
```

**Response (200 OK - Completed):**
```json
{
  "status": "qualified",
  "qualification_id": "qual_7x9k2m4p8n1",
  "model_id": "my-llama-70b-v1",
  "submitted_at": "2025-12-13T22:30:00Z",
  "verified_at": "2025-12-14T07:42:00Z",
  "verified_by": "firmus-verification-system-v2",
  "tier": "tier_1_efficient",
  "discount_percentage": 20.0,
  "qualified": true,
  "verified_metrics": {
    "avg_power_watts": 142.7,
    "peak_power_watts": 165.3,
    "power_cv": 0.089,
    "joules_per_token": 2.6,
    "tokens_per_joule": 0.385,
    "samples_tested": 20
  },
  "declared_vs_measured": {
    "avg_power_delta_percent": -1.7,
    "cv_delta_percent": -3.3,
    "within_tolerance": true
  },
  "reasoning": "Excellent power stability (CV=0.089) and low average power (142.7W). Qualifies for Tier 1.",
  "certificate_url": "https://certificates.firmus.ai/model-to-grid/qual_7x9k2m4p8n1.pdf",
  "valid_until": "2026-12-14T07:42:00Z"
}
```

**Response (200 OK - Failed):**
```json
{
  "status": "not_qualified",
  "qualification_id": "qual_7x9k2m4p8n1",
  "model_id": "my-llama-70b-v1",
  "tier": "tier_3_high_variance",
  "discount_percentage": 0.0,
  "qualified": false,
  "verified_metrics": {
    "avg_power_watts": 285.4,
    "power_cv": 0.182
  },
  "reasoning": "High power variance (CV=0.182) and high average power (285.4W). Standard pricing applies.",
  "recommendations": [
    "Consider kernel fusion optimizations to reduce power spikes",
    "Implement KV-cache optimization to lower average power",
    "Retest after optimizations to potentially qualify for Tier 2"
  ]
}
```

---

### 3. List Model Qualifications

Retrieve all qualification requests for your account.

**Endpoint:** `GET /model-to-grid/qualifications`

**Query Parameters:**
- `status` (optional): Filter by status (`pending`, `verified`, `failed`, `all`)
- `limit` (optional): Number of results (default: 10, max: 100)
- `offset` (optional): Pagination offset

**Request Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "qualifications": [
    {
      "qualification_id": "qual_7x9k2m4p8n1",
      "model_id": "my-llama-70b-v1",
      "status": "qualified",
      "tier": "tier_1_efficient",
      "discount_percentage": 20.0,
      "submitted_at": "2025-12-13T22:30:00Z",
      "verified_at": "2025-12-14T07:42:00Z"
    },
    {
      "qualification_id": "qual_3m8n7k2x5p9",
      "model_id": "my-mistral-8b-v2",
      "status": "verification_in_progress",
      "submitted_at": "2025-12-14T10:15:00Z"
    }
  ],
  "pagination": {
    "total": 2,
    "limit": 10,
    "offset": 0,
    "has_more": false
  }
}
```

---

### 4. Get Current Pricing for Model

Retrieve the active pricing tier for a qualified model.

**Endpoint:** `GET /model-to-grid/pricing/{model_id}`

**Request Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "model_id": "my-llama-70b-v1",
  "tier": "tier_1_efficient",
  "discount_percentage": 20.0,
  "base_price_per_1m_tokens": 50.00,
  "discounted_price_per_1m_tokens": 40.00,
  "annual_savings_estimate": "$12,450 (based on 10M tokens/month)",
  "qualification_valid_until": "2026-12-14T07:42:00Z",
  "certification_badge_url": "https://badges.firmus.ai/model-to-grid/tier-1/my-llama-70b-v1.svg"
}
```

---

### 5. Requalify Model

Request requalification for a model (required annually or after significant model changes).

**Endpoint:** `POST /model-to-grid/requalify/{model_id}`

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "reason": "model_updated",
  "changes_description": "Applied kernel fusion optimizations to reduce power variance",
  "updated_metrics": {
    "avg_power_watts": 138.5,
    "power_cv": 0.081
  }
}
```

**Response (202 Accepted):**
```json
{
  "status": "requalification_pending",
  "qualification_id": "qual_9p2k8m4x7n3",
  "model_id": "my-llama-70b-v1",
  "previous_tier": "tier_1_efficient",
  "submitted_at": "2025-12-15T14:20:00Z",
  "estimated_completion": "2025-12-17T10:00:00Z"
}
```

---

### 6. Webhook Notifications

Configure webhooks to receive real-time qualification updates.

**Endpoint:** `POST /webhooks/model-qualification`

**Webhook Payload (POST to your URL):**
```json
{
  "event": "qualification.completed",
  "qualification_id": "qual_7x9k2m4p8n1",
  "model_id": "my-llama-70b-v1",
  "timestamp": "2025-12-14T07:42:00Z",
  "status": "qualified",
  "tier": "tier_1_efficient",
  "discount_percentage": 20.0,
  "data_url": "https://api.firmus.ai/v1/model-to-grid/qualify/qual_7x9k2m4p8n1"
}
```

**Webhook Events:**
- `qualification.submitted` - Model submitted for qualification
- `qualification.in_progress` - Verification started
- `qualification.completed` - Qualification complete (success or failure)
- `qualification.expired` - Qualification expired (annual renewal required)

---

## Rate Limits

- **Qualification Submissions:** 10 per day per account
- **Status Checks:** 100 per hour
- **Pricing Lookups:** 1000 per hour

---

## Code Examples

### Python

```python
import requests

API_BASE = "https://api.firmus.ai/v1"
API_TOKEN = "your_firmus_api_token"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Submit model for qualification
payload = {
    "model_id": "my-llama-70b-v1",
    "model_name": "Custom Llama 70B",
    "architecture": "llama-3",
    "parameter_count": "70B",
    "declared_metrics": {
        "avg_power_watts": 145.2,
        "power_cv": 0.092
    },
    "contact_email": "dev@myorg.com"
}

response = requests.post(
    f"{API_BASE}/model-to-grid/qualify",
    json=payload,
    headers=headers
)

qualification_id = response.json()["qualification_id"]
print(f"Submitted! Qualification ID: {qualification_id}")

# Check status
status_response = requests.get(
    f"{API_BASE}/model-to-grid/qualify/{qualification_id}",
    headers=headers
)

print(status_response.json())
```

### cURL

```bash
# Submit qualification
curl -X POST https://api.firmus.ai/v1/model-to-grid/qualify \\
  -H "Authorization: Bearer your_firmus_api_token" \\
  -H "Content-Type: application/json" \\
  -d '{
    "model_id": "my-llama-70b-v1",
    "declared_metrics": {
      "avg_power_watts": 145.2,
      "power_cv": 0.092
    }
  }'

# Check status
curl https://api.firmus.ai/v1/model-to-grid/qualify/qual_7x9k2m4p8n1 \\
  -H "Authorization: Bearer your_firmus_api_token"
```

---

## SDK Support

Official SDKs available:
- **Python**: `pip install firmus-sdk`
- **JavaScript/TypeScript**: `npm install @firmus/sdk`
- **Go**: `go get github.com/firmus/go-sdk`

```python
from firmus_sdk import FirmusClient

client = FirmusClient(api_token="your_token")

# Submit qualification
qualification = client.model_to_grid.qualify(
    model_id="my-llama-70b-v1",
    declared_metrics={
        "avg_power_watts": 145.2,
        "power_cv": 0.092
    }
)

# Wait for completion
result = qualification.wait_for_completion()
print(f"Tier: {result.tier}, Discount: {result.discount_percentage}%")
```

---

## Support

- **Documentation**: https://docs.firmus.ai/model-to-grid
- **API Status**: https://status.firmus.ai
- **Support Email**: energy-efficiency@firmus.ai
- **Community Forum**: https://community.firmus.ai

---

*API Version: v1*  
*Last Updated: 2025-12-13*  
*Firmus AI Cloud Model-to-Grid Program*
