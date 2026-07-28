# MediMind – Data Flow

## Complete Request Flow

```
Step 1: User fills symptom form and clicks "Analyze Symptoms"
         ↓
Step 2: JavaScript validates input (non-empty, disclaimer checked)
         ↓
Step 3: Frontend sends POST request to backend
         POST /analyze
         Body: { "symptoms": "...", "duration": "...", "severity": "..." }
         ↓
Step 4: FastAPI receives and validates request (Pydantic schema)
         ↓
Step 5: Backend checks for emergency keywords
         ↓
Step 6: prompt_builder.py creates a safety-focused prompt
         ↓
Step 7: groq_service.py sends prompt to Groq API
         ↓
Step 8: Groq returns JSON with structured guidance
         ↓
Step 9: Backend wraps response with disclaimer and timestamp
         ↓
Step 10: Frontend receives JSON and renders guidance cards
```

## Request Example

```http
POST https://your-backend.onrender.com/analyze
Content-Type: application/json

{
  "symptoms": "Headache and mild fever for 2 days",
  "duration": "2 days",
  "severity": "mild"
}
```

## Response Example

```json
{
  "success": true,
  "guidance": {
    "summary": "Headaches with mild fever can be associated with...",
    "possible_causes": [
      "Viral infections such as the common cold",
      "Tension headaches",
      "Dehydration"
    ],
    "self_care_tips": [
      "Rest and stay hydrated",
      "Use a cool compress on your forehead",
      "Monitor your temperature"
    ],
    "when_to_seek_care": [
      "Fever above 103°F (39.4°C)",
      "Severe or sudden headache",
      "Symptoms lasting more than a week"
    ],
    "general_advice": "If symptoms worsen or new symptoms appear, consult a doctor."
  },
  "disclaimer": "This information is for educational purposes only...",
  "emergency_detected": false,
  "timestamp": "2026-07-26T17:25:00Z"
}
```

## Error Flow

If something fails (missing API key, network error, invalid input):

```
Backend returns → { "success": false, "error": "...", "code": "..." }
Frontend shows  → Red error message below the form
```

## Local vs Production URLs

| Environment | Frontend URL | Backend URL |
|-------------|--------------|-------------|
| Local       | http://localhost:5500 | http://localhost:8000 |
| Production  | https://medimind.vercel.app | https://medimind-api.onrender.com |

Configured in: `frontend/js/config.js` and `backend/.env` (ALLOWED_ORIGINS)
