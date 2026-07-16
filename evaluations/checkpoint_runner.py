from deepeval import evaluate
from deepeval.test_case import LLMTestCase

from checkpoints import ArchitectStage, EvaluationCheckpoint
from evaluation_settings import EvaluationSettings
from metric_profiles.requirement_interpretation_metrics import (
    build_requirement_interpretation_metrics,
)


class CheckpointRunner:
    """
    Evaluates an Architect lifecycle checkpoint using the
    semantic metrics configured for that stage.
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
        Convert an Architect checkpoint into a DeepEval
        single-turn test case.
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
        Select the DeepEval metrics appropriate for the
        checkpoint stage.
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

    def run(
        self,
        checkpoint: EvaluationCheckpoint,
    ):
        """
        Evaluate one Architect checkpoint.
        """

        test_case = self.build_test_case(checkpoint)
        metrics = self.build_metrics(checkpoint.stage)

        print("\nStarting Architect checkpoint evaluation")
        print("-" * 60)
        print(f"Checkpoint: {checkpoint.checkpoint_id}")
        print(f"Stage: {checkpoint.stage.value}")
        print(f"Metrics: {len(metrics)}")
        print()

        return evaluate(
            test_cases=[test_case],
            metrics=metrics,
            identifier=self.settings.run_identifier,
            hyperparameters={
                **self.settings.as_hyperparameters(),
                "checkpoint_id": checkpoint.checkpoint_id,
            },
        )