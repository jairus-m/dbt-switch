from pydantic import BaseModel, field_validator, model_validator
from typing import Dict
import re


class ProjectConfig(BaseModel):
    """Config for a single dbt Cloud project."""

    host: str
    project_id: int

    @field_validator("project_id")
    def validate_project_id(cls, v):
        if v <= 0:
            raise ValueError("Project ID must be a positive integer.")
        return v

    @field_validator("host")
    def validate_host(cls, v):
        """Validate host format without requiring protocol."""
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Host must be a non-empty string.")
        if v.isdigit() or ("." in v and v.replace(".", "").isdigit()):
            raise ValueError("Host must be a non-empty string. Not a number.")
        return v.strip()


class DbtSwitchConfig(BaseModel):
    """Main config file for dbt-switch."""

    profiles: Dict[str, ProjectConfig] = {}

    @field_validator("profiles")
    def validate_project_names(cls, v):
        """Validate project names are properly formatted."""
        for project_name in v.keys():
            if not isinstance(project_name, str) or not project_name.strip():
                raise ValueError("Project name must be a non-empty string.")

            if not re.match(r"^[a-zA-Z0-9_-]+$", project_name.strip()):
                raise ValueError(
                    f"Project name '{project_name}' contains invalid characters. Only letters, numbers, underscores, and hyphens are allowed."
                )
        return v

    @model_validator(mode="after")
    def validate_unique_constraints(cls, values):
        """Validate that each project has unique project ID and name."""
        if isinstance(values, DbtSwitchConfig):
            profiles = values.profiles
        else:
            profiles = values.get("profiles", {})

        # Check unique project IDs
        project_ids = [config.project_id for config in profiles.values()]
        if len(project_ids) != len(set(project_ids)):
            raise ValueError("Each project must have a unique project ID.")

        # Check unique project names (lowkey redundant since they're dict keys BUT explicit is better)
        project_names = list(profiles.keys())
        if len(project_names) != len(set(project_names)):
            raise ValueError("Each project must have a unique name.")

        return values
