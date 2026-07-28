# MediMind – Presentation Outline

Use this outline for your project presentation or report.

---

## Slide 1: Title

**MediMind – AI Healthcare Assistant**

- Your name / team
- Date
- Tech stack: HTML, CSS, JS | FastAPI | Groq

---

## Slide 2: Problem Statement

**The Problem:**
- Many people search symptoms online and find unreliable or alarming information.
- They need **clear, educational guidance** — not a replacement for a doctor.
- Access to basic health literacy should be simple and trustworthy.

**Our Solution:**
- A web app where users describe symptoms and receive **AI-generated educational health information**.
- Always includes medical disclaimers and encourages professional care.

---

## Slide 3: System Architecture

Show the three-tier diagram:

```
User → Frontend (Vercel) → Backend (Render) → Groq API → Response
```

**Key points:**
- Frontend = user interface only (no API keys)
- Backend = secure middle layer
- Groq = AI text generation

Reference: `docs/architecture.md`

---

## Slide 4: Why Groq?

| Reason | Explanation |
|--------|-------------|
| Natural language | Understands free-text symptom descriptions |
| Python SDK | Integrates easily with FastAPI |
| Free tier | Suitable for student/demo projects |
| Speed | `llama-3.3-70b-versatile` gives fast responses |
| JSON mode | Reliable structured output matching our schema |

**Alternatives considered:** OpenAI GPT, Anthropic Claude, Google Gemini — Groq chosen for speed and free tier.

---

## Slide 5: Data Flow Demo

Walk through the 10-step flow (see `docs/data-flow.md`):

1. User enters symptoms
2. Frontend validates and sends POST /analyze
3. Backend builds safety prompt
4. Groq generates JSON guidance
5. Frontend displays structured results

**Live demo:** Show the app running locally or deployed.

---

## Slide 6: Safety & Disclaimers

**How we keep it safe:**
- Prominent disclaimers on homepage and results
- User must check "I understand" before analyzing
- Prompt instructs AI: no diagnosis, no prescriptions
- Emergency keyword detection (chest pain, can't breathe, etc.)
- API key hidden on backend only

**What MediMind is NOT:**
- Not FDA-approved medical software
- Not a diagnosis tool
- Not for emergencies

---

## Slide 7: Limitations

1. **AI can be wrong** — responses may contain errors (hallucinations)
2. **No medical history** — doesn't know allergies, medications, age
3. **General information only** — not personalized medical advice
4. **Internet required** — depends on Groq API availability
5. **English only** — no multi-language support yet
6. **Not for emergencies** — users must call emergency services

---

## Slide 8: Future Enhancements

- User accounts and symptom history
- Multi-language support (Hindi, Spanish, etc.)
- Voice input for symptoms
- Integration with verified medical databases
- Stronger emergency detection with ML
- Mobile app (React Native / Flutter)
- Doctor referral directory

---

## Slide 9: Tech Stack Summary

| Layer | Technology | Deployment |
|-------|------------|------------|
| Frontend | HTML, CSS, JavaScript | Vercel |
| Backend | FastAPI (Python) | Render |
| AI | Groq (llama-3.3-70b-versatile) | Groq Cloud |
| Version Control | Git + GitHub | — |

---

## Slide 10: Conclusion

- MediMind demonstrates a **full-stack AI web application**
- Solves health literacy access with **responsible AI use**
- Clear architecture: **Frontend → Backend → Groq → User**
- Built with beginner-friendly, explainable code
- **Always consult a healthcare professional for medical decisions**

---

## Demo Checklist

Before presenting, verify:

- [ ] Backend running (`/health` returns OK)
- [ ] Frontend connected to backend
- [ ] Groq API key configured in `.env`
- [ ] Sample symptom analysis works end-to-end
- [ ] Disclaimer visible on page
- [ ] Responsive design works on mobile view
