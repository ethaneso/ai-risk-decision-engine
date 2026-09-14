from langchain.messages import SystemMessage

from src.app.agents.state import RiskAgentState
from src.app.agents.tools import get_risk_agent_tools
from src.app.services.llm.factory import get_chat_model


SYSTEM_PROMPT = """
You are the Risk Analysis Agent for the
AI Risk Decision Engine.

Your role is to answer cybersecurity,
governance, compliance, and risk questions.

You have three tools:

1. search_evidence
   Use when documentary evidence is needed.

2. query_risk_db
   Use when existing structured risk records
   or assessments are needed.

3. calculate_risk
   Use only when likelihood and impact are
   both known on the required 1-to-5 scale.

Mandatory rules:

- Prefer evidence over unsupported assumptions.
- Never invent database records.
- Never invent retrieved evidence.
- If a risk score is requested and both likelihood
  and impact are available, you MUST call calculate_risk.
- Never calculate likelihood multiplied by impact yourself.
- Never put a numerical risk score in an answer unless
  calculate_risk has been called.
- If documentary support is requested, call search_evidence.
- If search_evidence returns evidence, preserve it for
  the final response.
- If more information is required, use another tool.
- If available evidence is insufficient, say so.
- Do not invent controls, recommendations, or evidence
  that is not present in tool results.
"""


def reasoner_node(
    state: RiskAgentState,
):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ]

    tool_model = get_chat_model(
        mode=state.get("mode"), model=state.get("model")
    ).bind_tools(get_risk_agent_tools())

    response = tool_model.invoke(
        messages
    )

    return {
        "messages": [response]
    }
