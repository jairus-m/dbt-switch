from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Dict, List
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


class DbtCloudProjectItem(BaseModel):
    """A project item in the dbt_cloud.yml projects list."""

    project_name: str = Field(alias="project-name")
    project_id: str = Field(alias="project-id")
    account_name: str = Field(alias="account-name")
    account_id: str = Field(alias="account-id")
    account_host: str = Field(alias="account-host")
    token_name: str = Field(alias="token-name")
    token_value: str = Field(alias="token-value")

    model_config = ConfigDict(populate_by_name=True)


class DbtCloudContext(BaseModel):
    """Context section of dbt_cloud.yml."""

    active_host: str = Field(alias="active-host")
    active_project: str = Field(alias="active-project")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("active_host", "active_project")
    def validate_fields(cls, v):
        """Validate context fields."""
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Context fields must be non-empty strings.")
        return v.strip()


class DbtCloudConfig(BaseModel):
    """Main config file for dbt_cloud.yml."""

    version: str
    context: DbtCloudContext
    projects: List[DbtCloudProjectItem] = []

    @field_validator("version")
    def validate_version(cls, v):
        """Validate version format."""
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Version must be a non-empty string.")
        return v.strip()
