from deepeval import evaluate
from deepeval.test_case import LLMTestCase

from checkpoints import ArchitectStage, EvaluationCheckpoint
from deterministic_checks import (
    BaseDeterministicCheck,
    DeterministicCheckResult,
)
from evaluation_settings import EvaluationSettings
from metric_profiles.requirement_interpretation_metrics import (
    build_requirement_interpretation_metrics,
)


class CheckpointRunner:
    """
    Evaluates an Architect lifecycle checkpoint using semantic
    metrics and deterministic checks.
    """

    def __init__(
        self,
        settings: EvaluationSettings,
    ) -> None:
        self.settings = settings

    @staticmethod
    def build_test_case(
        checkpoint: EvaluationCheckpoint,
    ) -> LLMTestCase:
        """
        Convert an Architect checkpoint into a DeepEval test case.
        """

        return LLMTestCase(
            input=checkpoint.source_input,
            actual_output=checkpoint.actual_artifact,
            expected_output=checkpoint.expected_behavior,
        )

    def build_metrics(
        self,
        stage: ArchitectStage,
    ) -> list:
        """
        Select the semantic metrics for the checkpoint stage.
        """

        if stage == ArchitectStage.REQUIREMENT_INTERPRETATION:
            return build_requirement_interpretation_metrics(
                model=self.settings.judge_model,
                threshold=self.settings.semantic_threshold,
            )

        raise ValueError(
            f"No metric profile is configured for stage: "
            f"{stage.value}"
        )

    @staticmethod
    def run_deterministic_checks(
        checkpoint: EvaluationCheckpoint,
        checks: list[BaseDeterministicCheck],
    ) -> list[DeterministicCheckResult]:
        """
        Execute all exact rule-based checks for the checkpoint.
        """

        return [
            check.run(checkpoint)
            for check in checks
        ]

    @staticmethod
    def print_deterministic_results(
        results: list[DeterministicCheckResult],
    ) -> None:
        """
        Print deterministic check outcomes.
        """

        print("\nDeterministic validation")
        print("-" * 60)

        if not results:
            print("No deterministic checks configured.")
            return

        for result in results:
            status = "PASS" if result.passed else "FAIL"

            print(
                f"{result.check_name}: {status}"
            )
            print(f"Reason: {result.reason}")
            print()

    def run(
        self,
        checkpoint: EvaluationCheckpoint,
        deterministic_checks: (
            list[BaseDeterministicCheck] | None
        ) = None,
    ) -> dict:
        """
        Run semantic evaluation and deterministic validation
        for one Architect checkpoint.
        """

        configured_checks = deterministic_checks or []

        deterministic_results = (
            self.run_deterministic_checks(
                checkpoint=checkpoint,
                checks=configured_checks,
            )
        )

        deterministic_passed = all(
            result.passed
            for result in deterministic_results
        )

        self.print_deterministic_results(
            deterministic_results
        )

        test_case = self.build_test_case(checkpoint)
        metrics = self.build_metrics(checkpoint.stage)

        print("\nStarting semantic evaluation")
        print("-" * 60)
        print(f"Checkpoint: {checkpoint.checkpoint_id}")
        print(f"Stage: {checkpoint.stage.value}")
        print(f"Semantic metrics: {len(metrics)}")
        print()

        semantic_result = evaluate(
            test_cases=[test_case],
            metrics=metrics,
            identifier=self.settings.run_identifier,
            hyperparameters={
                **self.settings.as_hyperparameters(),
                "checkpoint_id": checkpoint.checkpoint_id,
            },
        )

        return {
            "checkpoint_id": checkpoint.checkpoint_id,
            "semantic_result": semantic_result,
            "deterministic_results": deterministic_results,
            "deterministic_passed": deterministic_passed,
        }