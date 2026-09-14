from langchain.messages import AIMessage
from langgraph.graph import (
    END,
    START,
    StateGraph,
)
from langgraph.prebuilt import ToolNode

from src.app.agents.nodes.finalizer import (
    finalizer_node,
)
from src.app.agents.nodes.reasoner import (
    reasoner_node,
)
from src.app.agents.nodes.tool_results import extract_tool_results
from src.app.agents.state import (
    RiskAgentState,
)
from src.app.agents.tools import get_risk_agent_tools


def route_after_reasoner(
    state: RiskAgentState,
) -> str:

    last_message = state[
        "messages"
    ][-1]

    if (
        isinstance(
            last_message,
            AIMessage,
        )
        and last_message.tool_calls
    ):
        return "tools"

    return "finalize"


def build_risk_agent():

    graph = StateGraph(
        RiskAgentState
    )

    graph.add_node(
        "reasoner",
        reasoner_node,
    )

    graph.add_node(
        "tools",
        ToolNode(
            get_risk_agent_tools()
        ),
    )

    graph.add_node(
        "finalize",
        finalizer_node,
    )

    graph.add_node(
        "extract_tool_results",
        extract_tool_results,
    )

    graph.add_edge(
        START,
        "reasoner",
    )

    graph.add_conditional_edges(
        "reasoner",
        route_after_reasoner,
        {
            "tools": "tools",
            "finalize": "finalize",
        },
    )

    graph.add_edge(
        "tools",
        "extract_tool_results",
    )

    graph.add_edge(
        "extract_tool_results",
        "reasoner",
    )

    graph.add_edge(
        "finalize",
        END,
    )

    return graph.compile()


risk_agent = build_risk_agent()
