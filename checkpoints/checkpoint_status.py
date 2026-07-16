from enum import Enum


class CheckpointStatus(str, Enum):
    """
    Represents the final quality-gate outcome for an
    Architect lifecycle checkpoint.
    """

    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"