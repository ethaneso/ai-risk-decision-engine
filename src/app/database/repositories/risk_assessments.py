from sqlalchemy import text

from src.app.database.connection import SessionLocal


def search_risk_assessments(
    search_term: str,
    limit: int = 5,
) -> list[dict]:

    with SessionLocal() as db:

        # Allows development before the risk_assessments
        # table has been introduced.
        table_exists = db.execute(
            text(
                """
                SELECT to_regclass(
                    'public.risk_assessments'
                )
                """
            )
        ).scalar()

        if table_exists is None:
            return []

        rows = db.execute(
            text(
                """
                SELECT
                    id,
                    title,
                    description,
                    risk_level,
                    inherent_risk_score,
                    residual_risk_score,
                    status
                FROM risk_assessments
                WHERE
                    title ILIKE :query
                    OR description ILIKE :query
                ORDER BY updated_at DESC
                LIMIT :limit
                """
            ),
            {
                "query": f"%{search_term}%",
                "limit": limit,
            },
        ).mappings()

        return [
            dict(row)
            for row in rows
        ]