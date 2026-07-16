import json
from dataclasses import dataclass
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from checkpoints.architect_stage import ArchitectStage
from checkpoints.evaluation_checkpoint import EvaluationCheckpoint
from deterministic_checks.base_check import BaseDeterministicCheck
from deterministic_checks.requirement_checks import (
    ForbiddenTermsCheck,
    RequiredTermsCheck,
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

        required_terms = cls._optional_string_list(
            item=item,
            field_name="required_terms",
            checkpoint_id=checkpoint_id,
        )

        forbidden_terms = cls._optional_string_list(
            item=item,
            field_name="forbidden_terms",
            checkpoint_id=checkpoint_id,
        )

        deterministic_checks: list[
            BaseDeterministicCheck
        ] = []

        if required_terms:
            deterministic_checks.append(
                RequiredTermsCheck(
                    required_terms=required_terms,
                )
            )

        if forbidden_terms:
            deterministic_checks.append(
                ForbiddenTermsCheck(
                    forbidden_terms=forbidden_terms,
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