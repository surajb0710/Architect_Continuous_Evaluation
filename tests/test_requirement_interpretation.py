from pathlib import Path

import pytest
from deepeval import assert_test

from data_loaders.requirement_interpretation_loader import (
    LoadedCheckpointCase,
    RequirementInterpretationDatasetLoader,
)
from evaluation_settings import EvaluationSettings
from evaluations.checkpoint_runner import CheckpointRunner


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_ROOT
    / "datasets"
    / "requirement_interpretation_regression.json"
)

SETTINGS = EvaluationSettings()

CASES = RequirementInterpretationDatasetLoader.load(
    DATASET_PATH
)


def checkpoint_case_id(
    case: LoadedCheckpointCase,
) -> str:
    """
    Use the checkpoint ID as the pytest test-case name.
    """

    return case.checkpoint.checkpoint_id


@pytest.mark.parametrize(
    "case",
    CASES,
    ids=checkpoint_case_id,
)
def test_requirement_interpretation(
    case: LoadedCheckpointCase,
) -> None:
    """
    Verify that one Architect requirement interpretation
    passes both deterministic and semantic quality gates.
    """

    runner = CheckpointRunner(
        settings=SETTINGS,
    )

    deterministic_results = (
        runner.run_deterministic_checks(
            checkpoint=case.checkpoint,
            checks=case.deterministic_checks,
        )
    )

    deterministic_failures = [
        result
        for result in deterministic_results
        if not result.passed
    ]

    failure_messages = [
        f"{result.check_name}: {result.reason}"
        for result in deterministic_failures
    ]

    assert not deterministic_failures, (
        f"Checkpoint '{case.checkpoint.checkpoint_id}' "
        f"failed deterministic validation:\n"
        + "\n".join(failure_messages)
    )

    test_case = runner.build_test_case(
        case.checkpoint
    )

    metrics = runner.build_metrics(
        stage=case.checkpoint.stage,
        threshold=(
            SETTINGS.semantic_warning_threshold
        ),
    )

    assert_test(
        test_case=test_case,
        metrics=metrics,
    )