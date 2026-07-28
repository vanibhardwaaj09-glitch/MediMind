# MediMind – System Architecture

## Overview

MediMind is a three-tier web application:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Browser   │────▶│   FastAPI   │────▶│   Groq API  │
│  (Frontend) │◀────│  (Backend)  │◀────│   (Groq)    │
└─────────────┘     └─────────────┘     └─────────────┘
     Vercel              Render           Groq Cloud
```

## Components

### 1. Frontend (HTML / CSS / JavaScript)
- **Hosted on:** Vercel (static files)
- **Role:** User interface — form, results display, disclaimers
- **Key files:**
  - `index.html` — page structure
  - `css/styles.css` — responsive design
  - `js/app.js` — form handling and API calls
  - `js/config.js` — API URL configuration

### 2. Backend (FastAPI / Python)
- **Hosted on:** Render
- **Role:** API server — validates input, calls Groq, returns JSON
- **Key files:**
  - `main.py` — routes (`/health`, `/analyze`)
  - `config.py` — environment variables
  - `models/schemas.py` — request/response data shapes
  - `services/prompt_builder.py` — AI prompt with safety rules
  - `services/groq_service.py` — Groq API integration

### 3. AI Layer (Groq)
- **Role:** Generates educational health guidance from structured prompts
- **Model:** `llama-3.3-70b-versatile` (fast, cost-effective for demos)
- **Security:** API key stored only on the backend

## Why This Architecture?

| Decision | Reason |
|----------|--------|
| Separate frontend & backend | Independent deployment; API key stays secure |
| FastAPI | Auto-generated docs, easy validation with Pydantic |
| Vanilla JS (no framework) | Beginner-friendly, easy to explain |
| Groq API | Fast inference, JSON mode, Python SDK |

## Security Notes

- Groq API key is **never** sent to the browser
- CORS restricts which frontend URLs can call the API
- Input length limits prevent abuse
- Prompt engineering reduces diagnostic language
