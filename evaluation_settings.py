from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationSettings:
    """
    Stores non-secret configuration for Architect checkpoint
    evaluation.
    """

    judge_model: str = "gpt-4.1-mini"
    semantic_threshold: float = 0.7

    run_identifier: str = (
        "architect-requirement-interpretation-evaluation"
    )

    dataset_version: str = "requirement-interpretation-v1"

    def __post_init__(self) -> None:
        if not 0 <= self.semantic_threshold <= 1:
            raise ValueError(
                "Semantic threshold must be between 0 and 1."
            )

        required_text_fields = {
            "judge_model": self.judge_model,
            "run_identifier": self.run_identifier,
            "dataset_version": self.dataset_version,
        }

        for field_name, field_value in required_text_fields.items():
            if not isinstance(field_value, str) or not field_value.strip():
                raise ValueError(
                    f"Setting '{field_name}' must be "
                    f"a non-empty string."
                )

    def as_hyperparameters(self) -> dict[str, str | float]:
        """
        Return metadata describing this evaluation run.
        """

        return {
            "architect_stage": "requirement_interpretation",
            "judge_model": self.judge_model,
            "semantic_threshold": self.semantic_threshold,
            "dataset_version": self.dataset_version,
        }