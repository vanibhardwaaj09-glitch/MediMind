"""
MediMind – Prompt Builder
---------------------------
Builds the prompt sent to Groq.
Includes strict safety rules so the AI provides educational guidance only.
"""

from models.schemas import AnalyzeRequest


# Keywords that may indicate a medical emergency.
# If found, the backend flags the response with emergency_detected=True.
EMERGENCY_KEYWORDS = [
    "chest pain",
    "heart attack",
    "can't breathe",
    "cannot breathe",
    "difficulty breathing",
    "severe bleeding",
    "unconscious",
    "stroke",
    "seizure",
    "suicidal",
    "overdose",
]


def check_emergency_keywords(symptoms_text: str) -> bool:
    """
    Checks if the user's symptoms text contains emergency-related keywords.
    Returns True if any keyword is found (case-insensitive).
    """
    lower_text = symptoms_text.lower()
    return any(keyword in lower_text for keyword in EMERGENCY_KEYWORDS)


def build_prompt(request: AnalyzeRequest) -> str:
    """
    Creates the full prompt string sent to Groq.

    The prompt instructs the AI to:
    - Provide EDUCATIONAL information only
    - Never diagnose or prescribe
    - Return structured JSON matching our GuidanceContent schema
    """

    # Build optional context lines from duration/severity fields
    extra_context = ""
    if request.duration:
        extra_context += f"\nDuration: {request.duration}"
    if request.severity:
        extra_context += f"\nSeverity: {request.severity}"

    prompt = f"""You are MediMind, an AI healthcare education assistant.

STRICT RULES — YOU MUST FOLLOW ALL OF THESE:
1. Provide EDUCATIONAL health information ONLY. You are NOT a doctor.
2. NEVER diagnose the user or say "you have [condition]".
3. NEVER prescribe medications or specific dosages.
4. Use phrases like "may be associated with", "could be related to", "some people experience".
5. Always encourage consulting a healthcare professional.
6. Keep language simple, clear, and beginner-friendly.
7. If symptoms sound urgent or emergency-related, strongly advise seeking immediate medical care.

USER'S SYMPTOMS:
{request.symptoms}{extra_context}

Respond ONLY with valid JSON in this exact structure (no markdown, no extra text):
{{
  "summary": "A brief 2-3 sentence educational overview of the symptoms described.",
  "possible_causes": [
    "General consideration 1 (not a diagnosis)",
    "General consideration 2",
    "General consideration 3"
  ],
  "self_care_tips": [
    "General self-care tip 1",
    "General self-care tip 2",
    "General self-care tip 3"
  ],
  "when_to_seek_care": [
    "Sign or reason to see a doctor 1",
    "Sign or reason to see a doctor 2"
  ],
  "general_advice": "1-2 sentences of additional educational advice and reminder to consult a doctor."
}}
"""
    return prompt
