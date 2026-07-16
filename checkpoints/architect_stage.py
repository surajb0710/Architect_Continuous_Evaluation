from enum import Enum


class ArchitectStage(str, Enum):
    """
    Represents a stage in the Architect.new application
    generation lifecycle.
    """

    REQUIREMENT_INTERPRETATION = "requirement_interpretation"
    APPLICATION_STRUCTURE = "application_structure"
    CONFIGURATION = "configuration"
    GENERATED_IMPLEMENTATION = "generated_implementation"
    PREVIEW = "preview"
    CORRECTION = "correction"
    DEPLOYMENT = "deployment"
    FINAL_APPLICATION = "final_application"