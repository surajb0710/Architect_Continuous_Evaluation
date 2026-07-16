from abc import ABC, abstractmethod

from checkpoints.evaluation_checkpoint import EvaluationCheckpoint
from deterministic_checks.check_result import (
    DeterministicCheckResult,
)


class BaseDeterministicCheck(ABC):
    """
    Defines the contract for exact, rule-based checkpoint checks.
    """

    @abstractmethod
    def run(
        self,
        checkpoint: EvaluationCheckpoint,
    ) -> DeterministicCheckResult:
        """
        Execute the check against an evaluation checkpoint.
        """

        raise NotImplementedError