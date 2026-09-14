import json
from typing import Any

from langchain.messages import ToolMessage

from src.app.agents.state import RiskAgentState


def _message_payload(content: Any) -> dict[str, Any] | None:
    if isinstance(content, dict):
        return content

    if not isinstance(content, str):
        return None

    try:
        payload = json.loads(content)
    except (TypeError, json.JSONDecodeError):
        return None

    return payload if isinstance(payload, dict) else None


def extract_tool_results(state: RiskAgentState):
    """Persist authoritative tool outputs as structured graph state."""
    evidence = list(state.get("evidence", []))
    risk_calculation = state.get("risk_calculation")
    tools_used = list(state.get("tools_used", []))

    for message in state["messages"]:
        if not isinstance(message, ToolMessage) or not message.name:
            continue

        if message.name not in tools_used:
            tools_used.append(message.name)

        payload = _message_payload(message.content)
        if payload is None:
            continue

        if message.name == "search_evidence":
            returned_evidence = payload.get("evidence")
            if isinstance(returned_evidence, list):
                evidence = returned_evidence
        elif message.name == "calculate_risk":
            risk_calculation = payload

    return {
        "evidence": evidence,
        "risk_calculation": risk_calculation,
        "tools_used": tools_used,
    }
