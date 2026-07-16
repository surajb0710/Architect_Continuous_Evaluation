from checkpoints import ArchitectStage, EvaluationCheckpoint
from deterministic_checks import (
    ForbiddenTermsCheck,
    RequiredTermsCheck,
)
from evaluation_settings import EvaluationSettings
from evaluations import CheckpointRunner


def print_checkpoint_result(result) -> None:
    """
    Print the combined semantic and deterministic outcome.
    """

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
    print(f"Semantic passed      : {result.semantic_passed}")
    print(
        f"Deterministic passed : "
        f"{result.deterministic_passed}"
    )
    print(f"Checkpoint status    : {result.status.value.upper()}")


def main() -> None:
    settings = EvaluationSettings()

    checkpoint = EvaluationCheckpoint(
        checkpoint_id="REQ-001",
        stage=ArchitectStage.REQUIREMENT_INTERPRETATION,
        source_input=(
            "Build a customer-support application that answers "
            "questions only from uploaded company policy documents. "
            "When the requested information is unavailable, the "
            "application must clearly say that it cannot find the "
            "answer and must not invent company policy."
        ),
        actual_artifact=(
            "Create a customer-support assistant connected to uploaded "
            "company policy documents. The assistant should answer "
            "employee questions using those policy documents. If the "
            "answer cannot be found, it should clearly state that the "
            "information is unavailable rather than guessing."
        ),
        expected_behavior=(
            "The interpretation must preserve the customer-support "
            "purpose, document-only grounding, uploaded company policy "
            "documents, missing-information behaviour, and prohibition "
            "against inventing company policy."
        ),
        metadata={
            "dataset_version": settings.dataset_version,
            "capture_method": "manual",
        },
    )

    deterministic_checks = [
        RequiredTermsCheck(
            required_terms=[
                "policy documents",
            ]
        ),
        ForbiddenTermsCheck(
            forbidden_terms=[
                "internet search",
                "general-purpose chatbot",
            ]
        ),
    ]

    runner = CheckpointRunner(settings=settings)

    result = runner.run(
        checkpoint=checkpoint,
        deterministic_checks=deterministic_checks,
    )

    print_checkpoint_result(result)


if __name__ == "__main__":
    main()