"""
MediMind – Pydantic Schemas (Data Models)
-----------------------------------------
These classes define the shape of data sent TO and FROM the API.
FastAPI uses them for automatic validation and documentation.
"""

from typing import Optional
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """
    Data the frontend sends when the user clicks 'Analyze Symptoms'.

    Example:
        {
            "symptoms": "Headache and fever for 2 days",
            "duration": "2 days",
            "severity": "mild"
        }
    """

    # Required: what the user is experiencing
    symptoms: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Description of the user's symptoms",
        examples=["Headache and mild fever for 2 days"],
    )

    # Optional extra context to improve AI guidance
    duration: Optional[str] = Field(
        None,
        max_length=100,
        description="How long symptoms have been present",
        examples=["2 days"],
    )

    severity: Optional[str] = Field(
        None,
        description="Severity level: mild, moderate, or severe",
        examples=["mild"],
    )


class GuidanceContent(BaseModel):
    """
    Structured educational guidance returned by the AI.
    Each field maps to a section shown on the frontend.
    """

    summary: str = Field(..., description="Brief overview of the guidance")
    possible_causes: list[str] = Field(
        default_factory=list,
        description="General possible considerations (not a diagnosis)",
    )
    self_care_tips: list[str] = Field(
        default_factory=list,
        description="General self-care suggestions",
    )
    when_to_seek_care: list[str] = Field(
        default_factory=list,
        description="Signs that warrant seeing a healthcare provider",
    )
    general_advice: str = Field(
        default="",
        description="Additional general educational advice",
    )


class AnalyzeResponse(BaseModel):
    """
    Data the backend sends back to the frontend after analysis.

    Example:
        {
            "success": true,
            "guidance": { ... },
            "disclaimer": "...",
            "emergency_detected": false,
            "timestamp": "2026-07-26T17:25:00Z"
        }
    """

    success: bool = True
    guidance: GuidanceContent
    disclaimer: str
    emergency_detected: bool = False
    timestamp: str


class ErrorResponse(BaseModel):
    """Returned when something goes wrong (validation error, API failure, etc.)."""

    success: bool = False
    error: str
    code: str = "ERROR"
