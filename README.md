# MediMind – AI Healthcare Assistant

A beginner-friendly web application where users enter symptoms and receive **AI-generated educational health guidance** using Groq's LLM API.

> **Important:** MediMind is **NOT** a diagnosis tool and does **NOT** replace professional medical advice. Always consult a qualified healthcare provider.

---

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Frontend   | HTML, CSS, JavaScript               |
| Backend    | FastAPI (Python)                    |
| AI         | Groq (llama-3.3-70b-versatile)      |
| Deployment | Render (frontend + backend)         |

---

## Project Structure

```
medimind/
├── frontend/              → Static website (deploy to Render)
│   ├── index.html
│   ├── css/styles.css
│   ├── js/app.js
│   ├── js/config.js
│   └── vercel.json
├── backend/               → API server (deploy to Render)
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── runtime.txt
│   ├── Procfile
│   ├── models/schemas.py
│   └── services/
│       ├── groq_service.py
│       └── prompt_builder.py
├── render.yaml            → Render Blueprint (auto-deploys both services)
├── .gitignore
└── README.md
```

---

## How It Works (Data Flow)

```
User → Frontend → FastAPI (/analyze) → Groq API → FastAPI → Frontend → Display
```

1. User enters symptoms on the webpage.
2. Frontend sends a `POST` request to the backend.
3. Backend builds a safety-focused prompt and calls Groq.
4. Groq returns educational guidance (not a diagnosis).
5. Backend returns JSON to the frontend.
6. Frontend displays the response with a medical disclaimer.

---

## Local Setup

### Prerequisites

- Python 3.10 or newer
- A [Groq API key](https://console.groq.com/keys)

### 1. Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your GROQ_API_KEY
# (see Environment Variables section below)

# Run the server
uvicorn main:app --reload --port 8000
```

Backend runs at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### 2. Frontend

```bash
cd frontend
python -m http.server 5500
```

Open: `http://localhost:5500`

> The frontend automatically uses `http://localhost:8000` when running locally (see `js/config.js`).

---

## Environment Variables (Backend)

Create `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
DEFAULT_LLM_MODEL=llama-3.3-70b-versatile
```

| Variable           | Description                                      |
|--------------------|--------------------------------------------------|
| `GROQ_API_KEY`     | Your Groq API key (keep secret!)                 |
| `ALLOWED_ORIGINS`  | Comma-separated frontend URLs allowed by CORS    |
| `DEFAULT_LLM_MODEL`| LLM model name (default: `llama-3.3-70b-versatile`) |

---

## Deployment to Render

### Option A: Using Render Blueprint (Recommended)

1. Push this repo to GitHub.
2. Go to [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**.
3. Connect your GitHub repo.
4. Render reads `render.yaml` and creates **two services**:
   - `medimind-api` (Python web service)
   - `medimind-frontend` (Static site)
5. Set the **GROQ_API_KEY** environment variable on the `medimind-api` service:
   - Go to `medimind-api` → **Environment** → add `GROQ_API_KEY` with your key.
6. Wait for both services to deploy.
7. Update `frontend/js/config.js` with your actual backend URL (e.g., `https://medimind-api.onrender.com`).
8. Update `ALLOWED_ORIGINS` on the backend to include your frontend URL.

### Option B: Manual Setup

#### Backend

1. Create a new **Web Service** on [Render](https://render.com).
2. Connect your GitHub repo.
3. Settings:
   - **Name:** `medimind-api`
   - **Root Directory:** `backend`
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn main:app --workers 2 --bind 0.0.0.0:$PORT --timeout 120`
4. Add environment variables:
   - `GROQ_API_KEY` = your Groq API key
   - `ALLOWED_ORIGINS` = your frontend URL (e.g., `https://medimind-frontend.onrender.com`)
   - `DEFAULT_LLM_MODEL` = `llama-3.3-70b-versatile`
5. Deploy.

#### Frontend

1. Create a new **Static Site** on [Render](https://render.com).
2. Connect your GitHub repo.
3. Settings:
   - **Name:** `medimind-frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** `echo "Static site - no build needed"`
   - **Publish Directory:** `.`
4. Deploy.
5. Update `frontend/js/config.js` with your backend URL before pushing.

---

## API Endpoints

| Method | Endpoint   | Description                    |
|--------|------------|--------------------------------|
| GET    | `/health`  | Health check for deployment    |
| POST   | `/analyze` | Analyze symptoms with Groq     |

### Example Request

```json
POST /analyze
{
  "symptoms": "Headache and mild fever for 2 days",
  "duration": "2 days",
  "severity": "mild"
}
```

---

## Deployment Checklist

- [ ] `requirements.txt` has all dependencies pinned
- [ ] `Procfile` exists in `backend/` for gunicorn
- [ ] `runtime.txt` specifies Python version
- [ ] `render.yaml` is at the repo root
- [ ] `.env` is in `.gitignore` (never commit API keys)
- [ ] `GROQ_API_KEY` is set as an env var on Render
- [ ] `ALLOWED_ORIGINS` includes your frontend URL
- [ ] `frontend/js/config.js` has your production backend URL

---

## Limitations

- Educational information only — not medical advice or diagnosis
- AI responses may be incomplete or incorrect (hallucinations)
- Does not know your full medical history
- Not for medical emergencies — call emergency services if needed

---

## Future Enhancements

- User accounts and symptom history
- Multi-language support
- Voice input for symptoms
- Stronger emergency keyword detection
- Integration with verified medical knowledge bases

---

## License

Educational / portfolio project.
