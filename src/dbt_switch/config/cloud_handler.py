"""
File handler for the dbt_cloud.yml file. This includes operations to read and
modify the dbt_cloud.yml file for switching active host and project.
"""

import yaml
from pathlib import Path
from typing import Optional
from pydantic import ValidationError

from dbt_switch.utils.logger import logger
from dbt_switch.config.file_handler import get_project_config
from dbt_switch.validation.schemas import DbtCloudConfig


DBT_CLOUD_FILE = Path.home() / ".dbt" / "dbt_cloud.yml"


def read_dbt_cloud_config() -> Optional[DbtCloudConfig]:
    """
    Read and parse the dbt_cloud.yml file.
    Returns:
        DbtCloudConfig | None: Parsed config or None if file doesn't exist/is invalid
    """
    if not DBT_CLOUD_FILE.exists():
        logger.error(f"{DBT_CLOUD_FILE} does not exist")
        return None

    try:
        with open(DBT_CLOUD_FILE, "r") as file:
            raw_data = yaml.safe_load(file)
        return DbtCloudConfig(**raw_data)
    except ValidationError as e:
        logger.error(f"Error parsing {DBT_CLOUD_FILE}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error reading {DBT_CLOUD_FILE}: {e}")
        return None


def write_dbt_cloud_config(config: DbtCloudConfig) -> None:
    """
    Write a validated DbtCloudConfig to the YAML file.
    Args:
        config: DbtCloudConfig object
    """
    try:
        with open(DBT_CLOUD_FILE, "w") as file:
            # Use by_alias=True to preserve the original field names (with hyphens)
            yaml.dump(config.model_dump(by_alias=True), file, default_flow_style=False)
    except Exception as e:
        logger.error(f"Error writing {DBT_CLOUD_FILE}: {e}")
        raise


def update_dbt_cloud_config(
    config: DbtCloudConfig, new_host: str, new_project_id: str
) -> DbtCloudConfig:
    """
    Update the active host and project in a DbtCloudConfig.
    Args:
        config: Current DbtCloudConfig
        new_host: New host to set as active
        new_project_id: New project ID to set as active
    Returns:
        DbtCloudConfig: Updated config
    """
    # Update only the context - everything else stays the same
    config.context.active_host = new_host
    config.context.active_project = new_project_id

    return config


def switch_project(project_name: str) -> None:
    """
    Switch to a specific project by updating dbt_cloud.yml.
    Reads the project configuration from dbt_switch.yml and updates
    the active-host and active-project in dbt_cloud.yml.

    Args:
        project_name: Name of the project to switch to
    """
    try:
        project_config = get_project_config(project_name)
        if not project_config:
            raise ValueError(f"Project '{project_name}' not found in dbt_switch.yml")

        current_config = read_dbt_cloud_config()
        if not current_config:
            raise ValueError("Could not read dbt_cloud.yml file")

        updated_config = update_dbt_cloud_config(
            current_config, project_config.host, str(project_config.project_id)
        )

        write_dbt_cloud_config(updated_config)

        logger.info(f"Successfully switched to project '{project_name}'")
        logger.info(f"✓ Set active host: {project_config.host}")
        logger.info(f"✓ Set active project: {project_config.project_id}")

    except Exception as e:
        logger.error(f"Failed to switch to project '{project_name}': {e}")
        raise
