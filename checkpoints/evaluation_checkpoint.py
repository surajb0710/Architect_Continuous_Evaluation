from dataclasses import dataclass, field
from typing import Any

from checkpoints.architect_stage import ArchitectStage


@dataclass(frozen=True)
class EvaluationCheckpoint:
    """
    Represents one Architect.new lifecycle artefact that must
    be evaluated immediately after it is generated.
    """

    checkpoint_id: str
    stage: ArchitectStage

    source_input: str
    actual_artifact: str
    expected_behavior: str

    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Validate the checkpoint after it is created.
        """

        required_text_fields = {
            "checkpoint_id": self.checkpoint_id,
            "source_input": self.source_input,
            "actual_artifact": self.actual_artifact,
            "expected_behavior": self.expected_behavior,
        }

        for field_name, field_value in required_text_fields.items():
            if not isinstance(field_value, str) or not field_value.strip():
                raise ValueError(
                    f"Checkpoint field '{field_name}' "
                    f"must be a non-empty string."
                )