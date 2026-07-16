from checkpoints import ArchitectStage, EvaluationCheckpoint
from deterministic_checks import (
    ForbiddenTermsCheck,
    RequiredTermsCheck,
)
from evaluation_settings import EvaluationSettings
from evaluations import CheckpointRunner


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

    print("\nCheckpoint deterministic outcome")
    print("-" * 60)
    print(
        "PASS"
        if result["deterministic_passed"]
        else "FAIL"
    )


if __name__ == "__main__":
    main()