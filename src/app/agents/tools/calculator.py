from langchain.tools import tool

from src.app.risk.scoring import calculate_risk_score


@tool
def calculate_risk(
    likelihood: int,
    impact: int,
) -> dict:
    """
    Calculate a deterministic cybersecurity risk score.

    Use this tool when both likelihood and impact have
    been established on a 1-to-5 scale.

    Do not estimate likelihood or impact inside this tool.
    """

    result = calculate_risk_score(
        likelihood=likelihood,
        impact=impact,
    )

    return {
        "likelihood": result.likelihood,
        "impact": result.impact,
        "risk_score": result.score,
        "risk_level": result.level,
    }