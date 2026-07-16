from checkpoints.evaluation_checkpoint import EvaluationCheckpoint
from deterministic_checks.base_check import (
    BaseDeterministicCheck,
)
from deterministic_checks.check_result import (
    DeterministicCheckResult,
)


class RequiredTermsCheck(BaseDeterministicCheck):
    """
    Verifies that all required literal terms are present in
    the generated artefact.
    """

    def __init__(
        self,
        required_terms: list[str],
        case_sensitive: bool = False,
    ) -> None:
        if not required_terms:
            raise ValueError(
                "At least one required term must be provided."
            )

        self.required_terms = required_terms
        self.case_sensitive = case_sensitive

    def run(
        self,
        checkpoint: EvaluationCheckpoint,
    ) -> DeterministicCheckResult:
        artifact = checkpoint.actual_artifact

        if not self.case_sensitive:
            artifact = artifact.lower()

        missing_terms: list[str] = []

        for term in self.required_terms:
            search_term = (
                term
                if self.case_sensitive
                else term.lower()
            )

            if search_term not in artifact:
                missing_terms.append(term)

        if missing_terms:
            return DeterministicCheckResult(
                check_name="Required Terms",
                passed=False,
                reason=(
                    "Missing required terms: "
                    + ", ".join(missing_terms)
                ),
            )

        return DeterministicCheckResult(
            check_name="Required Terms",
            passed=True,
            reason="All required terms are present.",
        )


class ForbiddenTermsCheck(BaseDeterministicCheck):
    """
    Verifies that prohibited literal terms are not present in
    the generated artefact.
    """

    def __init__(
        self,
        forbidden_terms: list[str],
        case_sensitive: bool = False,
    ) -> None:
        if not forbidden_terms:
            raise ValueError(
                "At least one forbidden term must be provided."
            )

        self.forbidden_terms = forbidden_terms
        self.case_sensitive = case_sensitive

    def run(
        self,
        checkpoint: EvaluationCheckpoint,
    ) -> DeterministicCheckResult:
        artifact = checkpoint.actual_artifact

        if not self.case_sensitive:
            artifact = artifact.lower()

        detected_terms: list[str] = []

        for term in self.forbidden_terms:
            search_term = (
                term
                if self.case_sensitive
                else term.lower()
            )

            if search_term in artifact:
                detected_terms.append(term)

        if detected_terms:
            return DeterministicCheckResult(
                check_name="Forbidden Terms",
                passed=False,
                reason=(
                    "Detected forbidden terms: "
                    + ", ".join(detected_terms)
                ),
            )

        return DeterministicCheckResult(
            check_name="Forbidden Terms",
            passed=True,
            reason="No forbidden terms were detected.",
        )