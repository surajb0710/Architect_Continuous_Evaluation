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
        name="Unsupported Assumptions",
        criteria=(
            "Evaluate whether the actual output introduces material "
            "features, business rules, users, integrations, data "
            "sources, permissions, technical decisions, or constraints "
            "that are not supported by the input. Reasonable wording "
            "clarifications are acceptable, but invented requirements "
            "or unjustified design decisions must be penalized."
        ),
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.EXPECTED_OUTPUT,
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