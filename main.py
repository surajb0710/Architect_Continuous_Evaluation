from checkpoints import ArchitectStage, EvaluationCheckpoint
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
            "employee questions using those documents. If the answer "
            "cannot be found in the documents, it should clearly state "
            "that the information is unavailable rather than guessing."
        ),
        expected_behavior=(
            "The interpretation must preserve the customer-support "
            "purpose, document-only grounding, use of uploaded company "
            "policy documents, explicit missing-information behaviour, "
            "and prohibition against inventing company policy. It must "
            "not introduce unsupported integrations or business rules."
        ),
        metadata={
            "dataset_version": settings.dataset_version,
            "capture_method": "manual",
        },
    )

    runner = CheckpointRunner(settings=settings)

    runner.run(checkpoint)


if __name__ == "__main__":
    main()