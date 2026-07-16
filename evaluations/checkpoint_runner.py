from typing import Any

from deepeval import evaluate
from deepeval.test_case import LLMTestCase

from checkpoints import (
    ArchitectStage,
    CheckpointResult,
    CheckpointStatus,
    EvaluationCheckpoint,
    SemanticMetricResult,
)
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
            threshold: float | None = None,
    ) -> list:
        """
        Select semantic metrics for the checkpoint stage.

        A custom threshold may be supplied for stricter
        regression quality gates.
        """

        effective_threshold = (
            self.settings.semantic_threshold
            if threshold is None
            else threshold
        )

        if not 0 <= effective_threshold <= 1:
            raise ValueError(
                "Metric threshold must be between 0 and 1."
            )

        if stage == ArchitectStage.REQUIREMENT_INTERPRETATION:
            return build_requirement_interpretation_metrics(
                model=self.settings.judge_model,
                threshold=effective_threshold,
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
        Execute every exact rule-based check.
        """

        return [
            check.run(checkpoint)
            for check in checks
        ]

    @staticmethod
    def extract_semantic_results(
        evaluation_result: Any,
    ) -> list[SemanticMetricResult]:
        """
        Convert DeepEval metric data into framework-owned
        semantic result objects.
        """

        test_results = getattr(
            evaluation_result,
            "test_results",
            None,
        )

        if not test_results:
            raise RuntimeError(
                "DeepEval did not return any test results."
            )

        metric_data_items = getattr(
            test_results[0],
            "metrics_data",
            None,
        )

        if not metric_data_items:
            raise RuntimeError(
                "DeepEval did not return any metric results."
            )

        semantic_results: list[SemanticMetricResult] = []

        for metric_data in metric_data_items:
            score = getattr(metric_data, "score", None)

            if score is None:
                raise RuntimeError(
                    f"Metric '{metric_data.name}' did not "
                    f"return a score."
                )

            reason = getattr(
                metric_data,
                "reason",
                None,
            )

            error = getattr(
                metric_data,
                "error",
                None,
            )

            normalized_reason = (
                reason
                or error
                or "No evaluation reason was provided."
            )

            semantic_results.append(
                SemanticMetricResult(
                    metric_name=metric_data.name,
                    score=float(score),
                    threshold=float(metric_data.threshold),
                    passed=bool(metric_data.success),
                    reason=str(normalized_reason),
                )
            )

        return semantic_results

    def determine_status(
        self,
        semantic_results: list[SemanticMetricResult],
        deterministic_results: list[
            DeterministicCheckResult
        ],
    ) -> CheckpointStatus:
        """
        Calculate the final checkpoint quality-gate status.
        """

        semantic_passed = all(
            result.passed
            for result in semantic_results
        )

        deterministic_passed = all(
            result.passed
            for result in deterministic_results
        )

        if not semantic_passed or not deterministic_passed:
            return CheckpointStatus.FAIL

        warning_threshold = (
            self.settings.semantic_warning_threshold
        )

        has_borderline_semantic_score = any(
            result.score < warning_threshold
            for result in semantic_results
        )

        if has_borderline_semantic_score:
            return CheckpointStatus.WARNING

        return CheckpointStatus.PASS

    def run(
        self,
        checkpoint: EvaluationCheckpoint,
        deterministic_checks: (
            list[BaseDeterministicCheck] | None
        ) = None,
    ) -> CheckpointResult:
        """
        Run semantic evaluation and deterministic validation
        and return one combined checkpoint result.
        """

        configured_checks = deterministic_checks or []

        deterministic_results = (
            self.run_deterministic_checks(
                checkpoint=checkpoint,
                checks=configured_checks,
            )
        )

        test_case = self.build_test_case(checkpoint)
        metrics = self.build_metrics(checkpoint.stage)

        print("\nStarting Architect checkpoint evaluation")
        print("-" * 60)
        print(f"Checkpoint: {checkpoint.checkpoint_id}")
        print(f"Stage: {checkpoint.stage.value}")
        print(f"Semantic metrics: {len(metrics)}")
        print(
            f"Deterministic checks: "
            f"{len(configured_checks)}"
        )
        print()

        evaluation_result = evaluate(
            test_cases=[test_case],
            metrics=metrics,
            identifier=self.settings.run_identifier,
            hyperparameters={
                **self.settings.as_hyperparameters(),
                "checkpoint_id": checkpoint.checkpoint_id,
            },
        )

        semantic_results = self.extract_semantic_results(
            evaluation_result
        )

        semantic_passed = all(
            result.passed
            for result in semantic_results
        )

        deterministic_passed = all(
            result.passed
            for result in deterministic_results
        )

        status = self.determine_status(
            semantic_results=semantic_results,
            deterministic_results=deterministic_results,
        )

        return CheckpointResult(
            checkpoint_id=checkpoint.checkpoint_id,
            stage=checkpoint.stage,
            status=status,
            semantic_results=semantic_results,
            deterministic_results=deterministic_results,
            semantic_passed=semantic_passed,
            deterministic_passed=deterministic_passed,
        )