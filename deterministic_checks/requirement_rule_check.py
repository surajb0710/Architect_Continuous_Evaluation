from checkpoints.evaluation_checkpoint import EvaluationCheckpoint
from deterministic_checks.base_check import BaseDeterministicCheck
from deterministic_checks.check_result import DeterministicCheckResult
from deterministic_checks.requirement_rule import (
    RequirementRule,
    RequirementRuleType,
)


class RequirementRuleCheck(BaseDeterministicCheck):
    """
    Executes one typed requirement rule against an Architect
    stage artefact.
    """

    def __init__(
        self,
        rule: RequirementRule,
    ) -> None:
        self.rule = rule

    def run(
        self,
        checkpoint: EvaluationCheckpoint,
    ) -> DeterministicCheckResult:
        artifact = self._normalize(
            checkpoint.actual_artifact
        )

        normalized_terms = [
            self._normalize(term)
            for term in self.rule.terms
        ]

        if self.rule.rule_type == RequirementRuleType.REQUIRED_ALL:
            return self._evaluate_required_all(
                artifact=artifact,
                normalized_terms=normalized_terms,
            )

        if self.rule.rule_type == RequirementRuleType.REQUIRED_ANY:
            return self._evaluate_required_any(
                artifact=artifact,
                normalized_terms=normalized_terms,
            )

        if self.rule.rule_type == RequirementRuleType.FORBIDDEN_ANY:
            return self._evaluate_forbidden_any(
                artifact=artifact,
                normalized_terms=normalized_terms,
            )

        raise ValueError(
            f"Unsupported requirement rule type: "
            f"{self.rule.rule_type.value}"
        )

    def _evaluate_required_all(
        self,
        artifact: str,
        normalized_terms: list[str],
    ) -> DeterministicCheckResult:
        missing_terms = [
            original_term
            for original_term, normalized_term in zip(
                self.rule.terms,
                normalized_terms,
            )
            if normalized_term not in artifact
        ]

        if missing_terms:
            return self._result(
                passed=False,
                reason=(
                    "Missing required terms: "
                    + ", ".join(missing_terms)
                ),
            )

        return self._result(
            passed=True,
            reason="All required terms are present.",
        )

    def _evaluate_required_any(
        self,
        artifact: str,
        normalized_terms: list[str],
    ) -> DeterministicCheckResult:
        matching_terms = [
            original_term
            for original_term, normalized_term in zip(
                self.rule.terms,
                normalized_terms,
            )
            if normalized_term in artifact
        ]

        if matching_terms:
            return self._result(
                passed=True,
                reason=(
                    "At least one accepted term is present: "
                    + ", ".join(matching_terms)
                ),
            )

        return self._result(
            passed=False,
            reason=(
                "None of the accepted terms were found: "
                + ", ".join(self.rule.terms)
            ),
        )

    def _evaluate_forbidden_any(
        self,
        artifact: str,
        normalized_terms: list[str],
    ) -> DeterministicCheckResult:
        detected_terms = [
            original_term
            for original_term, normalized_term in zip(
                self.rule.terms,
                normalized_terms,
            )
            if normalized_term in artifact
        ]

        if detected_terms:
            return self._result(
                passed=False,
                reason=(
                    "Detected forbidden terms: "
                    + ", ".join(detected_terms)
                ),
            )

        return self._result(
            passed=True,
            reason="No forbidden terms were detected.",
        )

    def _normalize(
        self,
        value: str,
    ) -> str:
        stripped_value = value.strip()

        if self.rule.case_sensitive:
            return stripped_value

        return stripped_value.lower()

    def _result(
        self,
        passed: bool,
        reason: str,
    ) -> DeterministicCheckResult:
        return DeterministicCheckResult(
            check_name=(
                f"{self.rule.rule_id} — "
                f"{self.rule.description}"
            ),
            passed=passed,
            reason=reason,
        )