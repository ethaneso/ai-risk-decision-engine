from langchain.tools import tool

from src.app.database.repositories.risk_assessments import (
    search_risk_assessments,
)


@tool
def query_risk_db(
    search_term: str,
    limit: int = 5,
) -> dict:
    """
    Search existing structured risk assessments.

    Use this tool when the user asks about previously
    recorded risks, assessments, scores, statuses,
    or historical risk decisions.
    """

    results = search_risk_assessments(
        search_term=search_term,
        limit=limit,
    )

    if not results:
        return {
            "status": "no_results",
            "message": (
                "No matching structured risk "
                "assessment was found."
            ),
            "results": [],
        }

    return {
        "status": "ok",
        "result_count": len(results),
        "results": results,
    }