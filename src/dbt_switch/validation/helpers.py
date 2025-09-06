"""
Validation helper functions for dbt-switch configuration.
"""

import re
from pydantic import ValidationError
from .schemas import DbtSwitchConfig, ProjectConfig


def validate_project_name_format(name: str) -> None:
    """
    Validate project name format.
    Args:
        name: Project name to validate
    Raises:
        ValueError: If project name is invalid
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Project name must be a non-empty string.")

    name = name.strip()
    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        raise ValueError(
            f"Project name '{name}' contains invalid characters. "
            "Only letters, numbers, underscores, and hyphens are allowed."
        )


def check_project_name_exists(config: DbtSwitchConfig, name: str) -> bool:
    """
    Check if a project name already exists in the configuration.
    Args:
        config: The dbt-switch configuration
        name: Project name to check
    Returns:
        True if project exists, False otherwise
    """
    return name.strip() in config.profiles


def validate_unique_project_id(
    config: DbtSwitchConfig, new_project_id: int, exclude_project: str = None
) -> None:
    """
    Validate that a project ID is unique in the configuration.
    Args:
        config: The dbt-switch configuration
        new_project_id: The project ID to validate
        exclude_project: Project name to exclude from uniqueness check (for updates)
    Raises:
        ValueError: If project ID is not unique
    """
    existing_project_ids = []
    for project_name, project_config in config.profiles.items():
        if exclude_project and project_name == exclude_project:
            continue
        existing_project_ids.append(project_config.project_id)

    if new_project_id in existing_project_ids:
        raise ValueError(
            f"Project ID {new_project_id} is already in use by another project."
        )


def validate_full_config_after_modification(config: DbtSwitchConfig) -> None:
    """
    Perform full validation on a config object after modification.
    This ensures all constraints are still met after changes.

    Args:
        config: The dbt-switch configuration to validate

    Raises:
        ValidationError: If configuration is invalid
    """
    try:
        # Purely to trigger all validation
        _ = DbtSwitchConfig(**config.model_dump())
    except ValidationError:
        raise


def create_validated_project_config(host: str, project_id: int) -> ProjectConfig:
    """
    Create a validated ProjectConfig instance.
    Args:
        host: Project host
        project_id: Project ID
    Returns:
        Validated ProjectConfig instance
    Raises:
        ValidationError: If configuration is invalid
    """
    return ProjectConfig(host=host, project_id=project_id)
