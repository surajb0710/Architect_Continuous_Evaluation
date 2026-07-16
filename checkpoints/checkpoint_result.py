from dataclasses import dataclass

from checkpoints.architect_stage import ArchitectStage
from checkpoints.checkpoint_status import CheckpointStatus
from checkpoints.semantic_metric_result import (
    SemanticMetricResult,
)
from deterministic_checks.check_result import (
    DeterministicCheckResult,
)


@dataclass(frozen=True)
class CheckpointResult:
    """
    Represents the complete outcome of evaluating one
    Architect lifecycle checkpoint.
    """

    checkpoint_id: str
    stage: ArchitectStage
    status: CheckpointStatus

    semantic_results: list[SemanticMetricResult]
    deterministic_results: list[DeterministicCheckResult]

    semantic_passed: bool
    deterministic_passed: bool

    @property
    def passed(self) -> bool:
        """
        Return True only when the checkpoint fully passes.
        """

        return self.status == CheckpointStatus.PASS

    @property
    def failed(self) -> bool:
        """
        Return True when the checkpoint has failed.
        """

        return self.status == CheckpointStatus.FAIL