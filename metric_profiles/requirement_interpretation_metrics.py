from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams


def build_requirement_interpretation_metrics(
    model: str,
    threshold: float,
) -> list[GEval]:
    """
    Build semantic metrics for evaluating whether Architect
    correctly interpreted the original application requirement.
    """

    completeness = GEval(
        name="Requirement Completeness",
        criteria=(
            "Evaluate whether the actual output captures all important "
            "functional requirements, non-functional requirements, "
            "constraints, actors, integrations, data requirements, "
            "and expected behaviours contained in the input and "
            "described by the expected output. Penalize omitted or "
            "weakened requirements."
        ),
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.EXPECTED_OUTPUT,
        ],
        model=model,
        threshold=threshold,
    )

    intent_alignment = GEval(
        name="Intent Alignment",
        criteria=(
            "Evaluate whether the actual output correctly represents "
            "the user's intended application and business objective. "
            "It must not materially misunderstand, distort, broaden, "
            "or narrow the purpose described in the input. Use the "
            "expected output as the interpretation requirements."
        ),
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.EXPECTED_OUTPUT,
        ],
        model=model,
        threshold=threshold,
    )

    constraint_preservation = GEval(
        name="Constraint Preservation",
        criteria=(
            "Evaluate whether every explicit restriction, boundary, "
            "mandatory rule, prohibited behaviour, required technology, "
            "named integration, output constraint, and failure behaviour "
            "from the input is preserved in the actual output. Use the "
            "expected output to identify the constraints that must be "
            "retained."
        ),
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.EXPECTED_OUTPUT,
        ],
        model=model,
        threshold=threshold,
    )

    unsupported_assumptions = GEval(
        name="Absence of Unsupported Assumptions",
        criteria=(
             "Evaluate only whether the actual output introduces material "
                "features, actors, integrations, business rules, permissions, "
                "technical decisions, or constraints that are unsupported by "
                "the input. Do not penalize missing requirements in this metric; "
                "omissions are evaluated by other metrics. Give a high score when "
                "no unsupported assumptions are introduced, even if the output "
                "is incomplete. Give a low score only when unsupported additions "
                "or invented decisions are present."
        ),
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
           # SingleTurnParams.EXPECTED_OUTPUT,
        ],
        model=model,
        threshold=threshold,
    )

    return [
        completeness,
        intent_alignment,
        constraint_preservation,
        unsupported_assumptions,
    ]