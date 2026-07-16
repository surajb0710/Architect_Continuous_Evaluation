from pathlib import Path

from checkpoints.checkpoint_result import CheckpointResult
from checkpoints.checkpoint_status import CheckpointStatus
from data_loaders.requirement_interpretation_loader import (
    RequirementInterpretationDatasetLoader,
)
from evaluation_settings import EvaluationSettings
from evaluations.checkpoint_runner import CheckpointRunner


DATASET_PATH = Path(
    "datasets/requirement_interpretation_regression.json"
)


def print_checkpoint_result(
    result: CheckpointResult,
) -> None:
    print("\n" + "=" * 70)
    print("CHECKPOINT RESULT")
    print("=" * 70)

    print(f"Checkpoint ID : {result.checkpoint_id}")
    print(f"Stage         : {result.stage.value}")
    print(f"Final Status  : {result.status.value.upper()}")

    print("\nSemantic evaluation")
    print("-" * 70)

    for metric in result.semantic_results:
        status = "PASS" if metric.passed else "FAIL"

        print(
            f"{metric.metric_name}: "
            f"{metric.score:.2f} "
            f"(threshold {metric.threshold:.2f}) "
            f"- {status}"
        )
        print(f"Reason: {metric.reason}")
        print()

    print("Deterministic validation")
    print("-" * 70)

    if not result.deterministic_results:
        print("No deterministic checks configured.")

    for check in result.deterministic_results:
        status = "PASS" if check.passed else "FAIL"

        print(f"{check.check_name}: {status}")
        print(f"Reason: {check.reason}")
        print()

    print("Combined outcome")
    print("-" * 70)
    print(
        f"Semantic passed      : "
        f"{result.semantic_passed}"
    )
    print(
        f"Deterministic passed : "
        f"{result.deterministic_passed}"
    )
    print(
        f"Checkpoint status    : "
        f"{result.status.value.upper()}"
    )


def print_run_summary(
    results: list[CheckpointResult],
) -> None:
    passed = sum(
        result.status == CheckpointStatus.PASS
        for result in results
    )

    warnings = sum(
        result.status == CheckpointStatus.WARNING
        for result in results
    )

    failed = sum(
        result.status == CheckpointStatus.FAIL
        for result in results
    )

    print("\n" + "=" * 70)
    print("EVALUATION RUN SUMMARY")
    print("=" * 70)
    print(f"Total checkpoints : {len(results)}")
    print(f"Passed            : {passed}")
    print(f"Warnings          : {warnings}")
    print(f"Failed            : {failed}")


def main() -> None:
    settings = EvaluationSettings()

    cases = (
        RequirementInterpretationDatasetLoader.load(
            DATASET_PATH
        )
    )

    print(
        f"Loaded {len(cases)} requirement "
        f"interpretation checkpoint(s)."
    )

    runner = CheckpointRunner(
        settings=settings,
    )

    results: list[CheckpointResult] = []

    for case in cases:
        result = runner.run(
            checkpoint=case.checkpoint,
            deterministic_checks=(
                case.deterministic_checks
            ),
        )

        results.append(result)
        print_checkpoint_result(result)

    print_run_summary(results)


if __name__ == "__main__":
    main()