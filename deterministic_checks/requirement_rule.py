from dataclasses import dataclass
from enum import Enum


class RequirementRuleType(str, Enum):
    """
    Types of exact rules that can be applied to an
    Architect requirement interpretation artefact.
    """

    REQUIRED_ALL = "required_all"
    REQUIRED_ANY = "required_any"
    FORBIDDEN_ANY = "forbidden_any"


@dataclass(frozen=True)
class RequirementRule:
    """
    Represents one exact, rule-based requirement validation.
    """

    rule_id: str
    rule_type: RequirementRuleType
    description: str
    terms: list[str]
    case_sensitive: bool = False

    def __post_init__(self) -> None:
        required_text_fields = {
            "rule_id": self.rule_id,
            "description": self.description,
        }

        for field_name, value in required_text_fields.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"Requirement rule field '{field_name}' "
                    f"must be a non-empty string."
                )

        if not self.terms:
            raise ValueError(
                f"Requirement rule '{self.rule_id}' "
                f"must contain at least one term."
            )

        for index, term in enumerate(self.terms):
            if not isinstance(term, str) or not term.strip():
                raise ValueError(
                    f"Requirement rule '{self.rule_id}' "
                    f"contains an invalid term at index {index}."
                )