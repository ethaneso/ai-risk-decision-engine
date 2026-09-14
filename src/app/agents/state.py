from typing import Any

from langgraph.graph import MessagesState


class RiskAgentState(MessagesState):
    """
    Shared state passed through the LangGraph workflow.
    """

    evidence: list[dict[str, Any]]
    risk_calculation: dict[str, Any] | None
    tools_used: list[str]
    final_response: dict[str, Any] | None
    mode: str | None
    model: str | None
