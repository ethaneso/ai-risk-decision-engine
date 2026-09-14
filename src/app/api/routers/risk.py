from fastapi import APIRouter
from langchain.messages import HumanMessage

from src.app.agents.graph import risk_agent
from src.app.schemas.risk_agent import (
    RiskAgentRequest,
    RiskAnalysisResponse,
)


router = APIRouter(
    prefix="/risk",
    tags=["risk"],
)


@router.post(
    "/analyze",
    response_model=RiskAnalysisResponse,
)
def analyze_risk(
    request: RiskAgentRequest,
):

    result = risk_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=request.question
                )
            ],
            "final_response": None,
            "evidence": [],
            "risk_calculation": None,
            "tools_used": [],
            "mode": request.mode,
            "model": request.model,
        }
    )

    return result[
        "final_response"
    ]
