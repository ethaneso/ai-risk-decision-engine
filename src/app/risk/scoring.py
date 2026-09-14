from dataclasses import dataclass


@dataclass(frozen=True)
class RiskScore:
    likelihood: int
    impact: int
    score: int
    level: str


def calculate_risk_score(
    likelihood: int,
    impact: int,
) -> RiskScore:

    if not 1 <= likelihood <= 5:
        raise ValueError(
            "likelihood must be between 1 and 5"
        )

    if not 1 <= impact <= 5:
        raise ValueError(
            "impact must be between 1 and 5"
        )

    score = likelihood * impact

    # Illustrative thresholds.
    # Replace later with your formal risk methodology.
    if score <= 4:
        level = "low"
    elif score <= 9:
        level = "medium"
    elif score <= 16:
        level = "high"
    else:
        level = "critical"

    return RiskScore(
        likelihood=likelihood,
        impact=impact,
        score=score,
        level=level,
    )