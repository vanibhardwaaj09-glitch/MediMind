"""
MediMind – Configuration
------------------------
Loads settings from environment variables (.env file).
Keeps sensitive data like API keys out of the source code.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()


class Settings:
    """Application settings read from environment variables."""

    # Groq API key (required)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Default LLM model for Groq
    DEFAULT_LLM_MODEL: str = os.getenv("DEFAULT_LLM_MODEL", "llama-3.3-70b-versatile")

    # Comma-separated frontend URLs for CORS (Cross-Origin Resource Sharing)
    ALLOWED_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:5500,http://127.0.0.1:5500"
        ).split(",")
        if origin.strip()
    ]

    # Maximum length of symptoms text (matches frontend limit)
    MAX_SYMPTOMS_LENGTH: int = 500

    # Standard medical disclaimer returned with every response
    MEDICAL_DISCLAIMER: str = (
        "This information is for educational purposes only and is NOT medical advice, "
        "a diagnosis, or a treatment plan. Always consult a qualified healthcare "
        "professional for medical concerns. In an emergency, call your local emergency number."
    )


# Single shared settings instance used across the app
settings = Settings()
