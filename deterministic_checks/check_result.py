from dataclasses import dataclass


@dataclass(frozen=True)
class DeterministicCheckResult:
    """
    Represents the outcome of one deterministic checkpoint check.
    """

    check_name: str
    passed: bool
    reason: str