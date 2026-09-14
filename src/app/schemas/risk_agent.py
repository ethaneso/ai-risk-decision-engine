from typing import Literal

from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    chunk_id: str | None = None
    document_id: str | None = None
    source: str | None = None

    content: str

    relevance_score: float | None = None


class RiskAgentRequest(BaseModel):
    question: str
    mode: Literal["offline", "online"] | None = None
    model: str | None = None


class RiskNarrative(BaseModel):
    answer: str
    risk_level: Literal[
        "low", "medium", "high", "critical", "unknown"
    ] = "unknown"
    confidence: float = Field(ge=0.0, le=1.0)
    limitations: list[str] = Field(default_factory=list)


class RiskAnalysisResponse(BaseModel):
    answer: str = Field(
        description="Evidence-grounded answer to the user's question."
    )

    risk_level: Literal[
        "low",
        "medium",
        "high",
        "critical",
        "unknown",
    ] = "unknown"

    risk_score: float | None = Field(
        default=None,
        description="Calculated risk score when sufficient inputs exist.",
    )

    evidence: list[EvidenceItem] = Field(
        default_factory=list,
    )

    tools_used: list[str] = Field(
        default_factory=list,
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence from 0 to 1.",
    )

    limitations: list[str] = Field(
        default_factory=list,
    )
