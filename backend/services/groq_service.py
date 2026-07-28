"""
MediMind – Groq AI Service
---------------------------
Handles all communication with Groq API.
The API key stays here on the backend — never exposed to the frontend.
"""

import json
from groq import Groq

from config import settings
from models.schemas import AnalyzeRequest, GuidanceContent
from services.prompt_builder import build_prompt


_client: Groq | None = None


def _get_groq_client() -> Groq:
    global _client
    if _client is None:
        if not settings.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not set. Add it to your .env file."
            )
        _client = Groq(api_key=settings.GROQ_API_KEY)
    return _client


def generate_health_guidance(request: AnalyzeRequest) -> GuidanceContent:
    """
    Sends the user's symptoms to Groq and returns structured guidance.

    Steps:
    1. Build a safety-focused prompt
    2. Call Groq API
    3. Parse the JSON response into a GuidanceContent object
    4. Return it to the route handler in main.py
    """

    # Step 1: Build the prompt with safety instructions
    prompt = build_prompt(request)

    # Step 2: Get Groq client and generate a response
    client = _get_groq_client()
    response = client.chat.completions.create(
        model=settings.DEFAULT_LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.4,
        response_format={"type": "json_object"},
    )

    # Step 3: Parse Groq's JSON text into a Python dictionary
    content = response.choices[0].message.content
    try:
        guidance_data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Groq returned invalid JSON: {content[:200]}"
        ) from exc

    # Step 4: Validate and return as a Pydantic model
    return GuidanceContent(
        summary=guidance_data.get("summary", "No summary available."),
        possible_causes=guidance_data.get("possible_causes", []),
        self_care_tips=guidance_data.get("self_care_tips", []),
        when_to_seek_care=guidance_data.get("when_to_seek_care", []),
        general_advice=guidance_data.get("general_advice", ""),
    )
