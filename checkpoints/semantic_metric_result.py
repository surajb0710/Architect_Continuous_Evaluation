from dataclasses import dataclass


@dataclass(frozen=True)
class SemanticMetricResult:
    """
    Represents one normalized DeepEval semantic metric result.
    """

    metric_name: str
    score: float
    threshold: float
    passed: bool
    reason: str