def get_risk_agent_tools():
    """Load all tools only when the complete agent is constructed."""
    from src.app.agents.tools.calculator import calculate_risk
    from src.app.agents.tools.database import query_risk_db
    from src.app.agents.tools.search import search_evidence

    return [search_evidence, query_risk_db, calculate_risk]
