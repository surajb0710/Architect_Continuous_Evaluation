import json
from dataclasses import dataclass
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from checkpoints.architect_stage import ArchitectStage
from checkpoints.evaluation_checkpoint import EvaluationCheckpoint
from deterministic_checks.base_check import BaseDeterministicCheck
from deterministic_checks.requirement_rule import (
    RequirementRule,
    RequirementRuleType,
)
from deterministic_checks.requirement_rule_check import (
    RequirementRuleCheck,
)


@dataclass
class LoadedCheckpointCase:
    """
    Represents one checkpoint loaded from the dataset,
    together with its configured deterministic checks.
    """

    checkpoint: EvaluationCheckpoint
    deterministic_checks: list[BaseDeterministicCheck]


class RequirementInterpretationDatasetLoader:
    """
    Loads requirement-interpretation checkpoint cases
    from a JSON dataset.
    """

    @classmethod
    def load(
        cls,
        dataset_path: str | Path,
    ) -> list[LoadedCheckpointCase]:
        path = Path(dataset_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Dataset file was not found: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Dataset path is not a file: {path}"
            )

        try:
            with path.open(
                mode="r",
                encoding="utf-8",
            ) as dataset_file:
                raw_data = json.load(dataset_file)
        except JSONDecodeError as error:
            raise ValueError(
                f"Dataset contains invalid JSON: {path}. "
                f"Line {error.lineno}, column {error.colno}."
            ) from error

        if not isinstance(raw_data, list):
            raise ValueError(
                "Dataset root must be a JSON array."
            )

        if not raw_data:
            raise ValueError(
                "Dataset must contain at least one checkpoint."
            )

        return [
            cls._build_case(item=item, index=index)
            for index, item in enumerate(raw_data)
        ]

    @classmethod
    def _build_case(
        cls,
        item: Any,
        index: int,
    ) -> LoadedCheckpointCase:
        if not isinstance(item, dict):
            raise ValueError(
                f"Dataset item at index {index} "
                f"must be a JSON object."
            )

        checkpoint_id = cls._required_string(
            item=item,
            field_name="checkpoint_id",
            index=index,
        )

        stage_value = cls._required_string(
            item=item,
            field_name="stage",
            index=index,
        )

        try:
            stage = ArchitectStage(stage_value)
        except ValueError as error:
            raise ValueError(
                f"Dataset item '{checkpoint_id}' contains "
                f"an unsupported stage: {stage_value}"
            ) from error

        if stage != ArchitectStage.REQUIREMENT_INTERPRETATION:
            raise ValueError(
                f"Dataset item '{checkpoint_id}' must use stage "
                f"'{ArchitectStage.REQUIREMENT_INTERPRETATION.value}'."
            )

        metadata = item.get("metadata", {})

        if not isinstance(metadata, dict):
            raise ValueError(
                f"Dataset item '{checkpoint_id}' field "
                f"'metadata' must be an object."
            )

        checkpoint = EvaluationCheckpoint(
            checkpoint_id=checkpoint_id,
            stage=stage,
            source_input=cls._required_string(
                item=item,
                field_name="source_input",
                index=index,
            ),
            actual_artifact=cls._required_string(
                item=item,
                field_name="actual_artifact",
                index=index,
            ),
            expected_behavior=cls._required_string(
                item=item,
                field_name="expected_behavior",
                index=index,
            ),
            metadata=metadata,
        )

        deterministic_checks = (
            cls._build_deterministic_checks(
                item=item,
                checkpoint_id=checkpoint_id,
            )
        )

        return LoadedCheckpointCase(
            checkpoint=checkpoint,
            deterministic_checks=deterministic_checks,
        )

    @staticmethod
    def _required_string(
        item: dict[str, Any],
        field_name: str,
        index: int,
    ) -> str:
        value = item.get(field_name)

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Dataset item at index {index} field "
                f"'{field_name}' must be a non-empty string."
            )

        return value.strip()

    @staticmethod
    def _optional_string_list(
        item: dict[str, Any],
        field_name: str,
        checkpoint_id: str,
    ) -> list[str]:
        value = item.get(field_name, [])

        if not isinstance(value, list):
            raise ValueError(
                f"Dataset item '{checkpoint_id}' field "
                f"'{field_name}' must be an array."
            )

        normalized_values: list[str] = []

        for list_index, list_item in enumerate(value):
            if (
                not isinstance(list_item, str)
                or not list_item.strip()
            ):
                raise ValueError(
                    f"Dataset item '{checkpoint_id}' field "
                    f"'{field_name}' contains an invalid value "
                    f"at index {list_index}."
                )

            normalized_values.append(
                list_item.strip()
            )

        return normalized_values

    @classmethod
    def _build_deterministic_checks(
            cls,
            item: dict[str, Any],
            checkpoint_id: str,
    ) -> list[BaseDeterministicCheck]:
        raw_rules = item.get(
            "deterministic_rules",
            [],
        )

        if not isinstance(raw_rules, list):
            raise ValueError(
                f"Dataset item '{checkpoint_id}' field "
                f"'deterministic_rules' must be an array."
            )

        checks: list[BaseDeterministicCheck] = []

        for rule_index, raw_rule in enumerate(raw_rules):
            rule = cls._build_requirement_rule(
                raw_rule=raw_rule,
                checkpoint_id=checkpoint_id,
                rule_index=rule_index,
            )

            checks.append(
                RequirementRuleCheck(rule=rule)
            )

        return checks

    @classmethod
    def _build_requirement_rule(
            cls,
            raw_rule: Any,
            checkpoint_id: str,
            rule_index: int,
    ) -> RequirementRule:
        if not isinstance(raw_rule, dict):
            raise ValueError(
                f"Dataset item '{checkpoint_id}' rule at "
                f"index {rule_index} must be an object."
            )

        rule_id = cls._required_rule_string(
            raw_rule=raw_rule,
            field_name="rule_id",
            checkpoint_id=checkpoint_id,
            rule_index=rule_index,
        )

        rule_type_value = cls._required_rule_string(
            raw_rule=raw_rule,
            field_name="type",
            checkpoint_id=checkpoint_id,
            rule_index=rule_index,
        )

        description = cls._required_rule_string(
            raw_rule=raw_rule,
            field_name="description",
            checkpoint_id=checkpoint_id,
            rule_index=rule_index,
        )

        try:
            rule_type = RequirementRuleType(
                rule_type_value
            )
        except ValueError as error:
            supported_types = ", ".join(
                rule_type.value
                for rule_type in RequirementRuleType
            )

            raise ValueError(
                f"Dataset item '{checkpoint_id}' rule "
                f"'{rule_id}' has unsupported type "
                f"'{rule_type_value}'. Supported types: "
                f"{supported_types}."
            ) from error

        terms = cls._rule_terms(
            raw_rule=raw_rule,
            checkpoint_id=checkpoint_id,
            rule_id=rule_id,
        )

        case_sensitive = raw_rule.get(
            "case_sensitive",
            False,
        )

        if not isinstance(case_sensitive, bool):
            raise ValueError(
                f"Dataset item '{checkpoint_id}' rule "
                f"'{rule_id}' field 'case_sensitive' "
                f"must be a boolean."
            )

        return RequirementRule(
            rule_id=rule_id,
            rule_type=rule_type,
            description=description,
            terms=terms,
            case_sensitive=case_sensitive,
        )

    @staticmethod
    def _required_rule_string(
            raw_rule: dict[str, Any],
            field_name: str,
            checkpoint_id: str,
            rule_index: int,
    ) -> str:
        value = raw_rule.get(field_name)

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Dataset item '{checkpoint_id}' rule at "
                f"index {rule_index} field '{field_name}' "
                f"must be a non-empty string."
            )

        return value.strip()

    @staticmethod
    def _rule_terms(
            raw_rule: dict[str, Any],
            checkpoint_id: str,
            rule_id: str,
    ) -> list[str]:
        terms = raw_rule.get("terms")

        if not isinstance(terms, list) or not terms:
            raise ValueError(
                f"Dataset item '{checkpoint_id}' rule "
                f"'{rule_id}' field 'terms' must be a "
                f"non-empty array."
            )

        normalized_terms: list[str] = []

        for term_index, term in enumerate(terms):
            if not isinstance(term, str) or not term.strip():
                raise ValueError(
                    f"Dataset item '{checkpoint_id}' rule "
                    f"'{rule_id}' contains an invalid term "
                    f"at index {term_index}."
                )

            normalized_terms.append(term.strip())

        return normalized_terms
