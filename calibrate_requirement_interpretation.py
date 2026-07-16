from pathlib import Path

from checkpoints.checkpoint_status import CheckpointStatus
from data_loaders.requirement_interpretation_loader import (
    LoadedCheckpointCase,
    RequirementInterpretationDatasetLoader,
)
from evaluation_settings import EvaluationSettings
from evaluations.checkpoint_runner import CheckpointRunner


DATASET_PATH = Path(
    "datasets/requirement_interpretation_calibration.json"
)


def get_expected_statuses(
    case: LoadedCheckpointCase,
) -> set[CheckpointStatus]:
    """
    Read and validate the expected checkpoint statuses
    configured for a calibration case.
    """

    raw_statuses = case.checkpoint.metadata.get(
        "expected_statuses"
    )

    if not isinstance(raw_statuses, list) or not raw_statuses:
        raise ValueError(
            f"Calibration case "
            f"'{case.checkpoint.checkpoint_id}' must define "
            f"a non-empty metadata.expected_statuses array."
        )

    expected_statuses: set[CheckpointStatus] = set()

    for raw_status in raw_statuses:
        if not isinstance(raw_status, str):
            raise ValueError(
                f"Calibration case "
                f"'{case.checkpoint.checkpoint_id}' contains "
                f"an invalid expected status."
            )

        try:
            expected_statuses.add(
                CheckpointStatus(raw_status)
            )
        except ValueError as error:
            supported_statuses = ", ".join(
                status.value
                for status in CheckpointStatus
            )

            raise ValueError(
                f"Calibration case "
                f"'{case.checkpoint.checkpoint_id}' contains "
                f"unsupported expected status "
                f"'{raw_status}'. Supported statuses: "
                f"{supported_statuses}."
            ) from error

    return expected_statuses


def format_expected_statuses(
    statuses: set[CheckpointStatus],
) -> str:
    return ", ".join(
        sorted(status.value.upper() for status in statuses)
    )


def main() -> None:
    settings = EvaluationSettings()

    cases = RequirementInterpretationDatasetLoader.load(
        DATASET_PATH
    )

    runner = CheckpointRunner(
        settings=settings,
    )

    mismatches: list[str] = []

    print(
        f"\nLoaded {len(cases)} calibration case(s)."
    )

    for case in cases:
        expected_statuses = get_expected_statuses(case)

        result = runner.run(
            checkpoint=case.checkpoint,
            deterministic_checks=(
                case.deterministic_checks
            ),
        )

        matched = result.status in expected_statuses

        status_label = "MATCH" if matched else "MISMATCH"

        print("\n" + "=" * 70)
        print("CALIBRATION RESULT")
        print("=" * 70)
        print(
            f"Checkpoint : "
            f"{case.checkpoint.checkpoint_id}"
        )
        print(
            f"Quality    : "
            f"{case.checkpoint.metadata.get('scenario_quality')}"
        )
        print(
            f"Expected   : "
            f"{format_expected_statuses(expected_statuses)}"
        )
        print(
            f"Actual     : "
            f"{result.status.value.upper()}"
        )
        print(f"Outcome    : {status_label}")

        print("\nSemantic scores")

        for metric in result.semantic_results:
            print(
                f"- {metric.metric_name}: "
                f"{metric.score:.2f}"
            )

        print("\nDeterministic checks")

        if not result.deterministic_results:
            print("- No deterministic checks configured")

        for check in result.deterministic_results:
            check_status = (
                "PASS"
                if check.passed
                else "FAIL"
            )

            print(
                f"- {check.check_name}: "
                f"{check_status}"
            )

        if not matched:
            mismatches.append(
                f"{case.checkpoint.checkpoint_id}: "
                f"expected "
                f"{format_expected_statuses(expected_statuses)}, "
                f"received {result.status.value.upper()}"
            )

    print("\n" + "=" * 70)
    print("CALIBRATION SUMMARY")
    print("=" * 70)
    print(f"Total cases : {len(cases)}")
    print(
        f"Matched     : "
        f"{len(cases) - len(mismatches)}"
    )
    print(f"Mismatched  : {len(mismatches)}")

    if mismatches:
        print("\nMismatches:")

        for mismatch in mismatches:
            print(f"- {mismatch}")

        raise SystemExit(1)

    print(
        "\nRequirement-interpretation metrics are "
        "classifying the controlled cases as expected."
    )


if __name__ == "__main__":
    main()