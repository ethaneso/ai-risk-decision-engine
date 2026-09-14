from langchain.messages import HumanMessage, SystemMessage

from src.app.agents.state import RiskAgentState
from src.app.schemas.risk_agent import (
    EvidenceItem,
    RiskAnalysisResponse,
    RiskNarrative,
)
from src.app.services.llm.factory import get_chat_model


FINALIZER_PROMPT = """
Produce only the narrative portion of the final risk analysis.

Use only information available in the
conversation and tool observations.

Do not invent evidence.

Never invent or reconstruct evidence, tools used, or a risk score.
Never state a numerical risk score unless a calculate_risk tool
result is present in the conversation.
If no deterministic calculation exists, risk_level may be your
qualitative interpretation or "unknown".

Confidence must be between 0 and 1.
"""


def finalizer_node(
    state: RiskAgentState,
):

    messages = [
        SystemMessage(
            content=FINALIZER_PROMPT
        ),
        *state["messages"],
        HumanMessage(
            content=(
                "Return the final validated "
                "risk analysis now."
            )
        ),
    ]

    structured_model = get_chat_model(
        mode=state.get("mode"), model=state.get("model")
    ).with_structured_output(RiskNarrative)

    narrative = structured_model.invoke(
        messages
    )

    risk_calculation = state.get("risk_calculation")
    evidence = []
    for item in state.get("evidence", []):
        relevance_score = item.get("rerank_score")
        if relevance_score is None:
            relevance_score = item.get("similarity")

        evidence.append(
            EvidenceItem(
                chunk_id=item.get("chunk_id"),
                document_id=item.get("document_id"),
                source=item.get("source"),
                content=item["content"],
                relevance_score=relevance_score,
            )
        )

    response = RiskAnalysisResponse(
        answer=narrative.answer,
        risk_level=(
            risk_calculation["risk_level"]
            if risk_calculation
            else narrative.risk_level
        ),
        risk_score=(
            risk_calculation["risk_score"]
            if risk_calculation
            else None
        ),
        evidence=evidence,
        tools_used=state.get("tools_used", []),
        confidence=narrative.confidence,
        limitations=narrative.limitations,
    )

    return {
        "final_response": (
            response.model_dump()
        )
    }
