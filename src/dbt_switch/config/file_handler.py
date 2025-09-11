"""
File handler for the dbt_switch.yml file. This includes all operations that
directlymodify the dbt_switch.yml file.
"""

from pathlib import Path
import yaml
from pydantic import ValidationError

from dbt_switch.utils.logger import logger
from dbt_switch.validation.schemas import DbtSwitchConfig, ProjectConfig
from dbt_switch.validation.helpers import (
    validate_project_name_format,
    check_project_name_exists,
    validate_unique_project_id,
    validate_full_config_after_modification,
    create_validated_project_config,
)

DIRECTORY = Path.home() / ".dbt"
CONFIG_FILE = DIRECTORY / "dbt_switch.yml"


def init_config() -> None:
    """
    Initialize the dbt_switch.yml file in the ~/.dbt directory.
    This file contains the active project and host for the dbt Cloud project.
    """
    if not CONFIG_FILE.exists():
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        default_config = {"profiles": {}}
        with open(CONFIG_FILE, "w") as file:
            yaml.dump(default_config, file)
        logger.info(f"Initialized {CONFIG_FILE}")
    else:
        logger.info(f"{CONFIG_FILE} already exists")


def get_config() -> DbtSwitchConfig | None:
    """
    Get the config from the dbt_switch.yml file in the ~/.dbt directory.
    Returns:
        DbtSwitchConfig | None
    """
    if not CONFIG_FILE.exists():
        logger.info(f"{CONFIG_FILE} does not exist")
        return None
    try:
        with open(CONFIG_FILE, "r") as file:
            raw_data = yaml.safe_load(file)
        return DbtSwitchConfig(**raw_data)
    except ValidationError as e:
        logger.error(f"Error parsing {CONFIG_FILE}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error parsing {CONFIG_FILE}: {e}")
        return None


def save_config(config: DbtSwitchConfig) -> None:
    """
    Save a validated DbtSwitchConfig to the YAML file.
    Args:
        config: DbtSwitchConfig object
    """
    with open(CONFIG_FILE, "w") as file:
        yaml.dump(config.model_dump(), file)


def add_config(project: str, host: str, project_id: int) -> None:
    """
    Add a project configuration to the dbt_switch.yml file.
    Each project has a host and project_id.
    Args:
        project: dbt project name that is used to select the host and project_id
        host: Active host (ex. https://cloud.getdbt.com)
        project_id: dbt project id
         - ex. https://cloud.getdbt.com/settings/accounts/<account_id>/pages/projects/<project_id>
    """
    try:
        validate_project_name_format(project)

        config = get_config()
        if config is None:
            config = DbtSwitchConfig()

        if check_project_name_exists(config, project):
            raise ValueError(f"Project '{project}' already exists in configuration.")

        validate_unique_project_id(config, project_id)

        new_project = create_validated_project_config(host=host, project_id=project_id)

        config.profiles[project] = new_project
        validate_full_config_after_modification(config)

        save_config(config)

        logger.info(
            f"Added project '{project}' with host '{new_project.host}' and project_id {new_project.project_id}"
        )

    except (ValidationError, ValueError) as e:
        logger.error(f"Invalid configuration for project '{project}': {e}")
        raise


def get_project_config(project: str) -> ProjectConfig | None:
    """
    Get configuration for a specific project.
    Args:
        project: dbt project name that is used to select the host and project_id
    Returns:
        ProjectConfig | None
    """
    config = get_config()
    if config and project in config.profiles:
        return config.profiles[project]
    else:
        logger.error(f"Project '{project}' not found in configuration")
    return None


def update_project_host(project: str, host: str) -> None:
    """
    Update the host for a specific project.
    Args:
        project: dbt project name that is used to select the host and project_id
        host: Active host (ex. https://cloud.getdbt.com)
    """
    try:
        config = get_config()
        if not config:
            raise ValueError("Configuration file not found or invalid.")

        if project not in config.profiles:
            raise ValueError(f"Project '{project}' not found in configuration.")

        existing_project = config.profiles[project]

        updated_project = create_validated_project_config(
            host=host, project_id=existing_project.project_id
        )

        config.profiles[project] = updated_project
        validate_full_config_after_modification(config)

        save_config(config)
        logger.info(f"Updated project '{project}' with host '{updated_project.host}'")

    except (ValidationError, ValueError) as e:
        logger.error(f"Failed to update host for project '{project}': {e}")
        raise


def update_project_id(project: str, project_id: int) -> None:
    """
    Update the project_id for a specific project.
    Args:
        project: dbt project name that is used to select the host and project_id
        project_id: dbt project id
          - ex. https://cloud.getdbt.com/settings/accounts/<account_id>/pages/projects/<project_id>
    """
    try:
        config = get_config()
        if not config:
            raise ValueError("Configuration file not found or invalid.")

        if project not in config.profiles:
            raise ValueError(f"Project '{project}' not found in configuration.")

        validate_unique_project_id(config, project_id, exclude_project=project)

        existing_project = config.profiles[project]

        updated_project = create_validated_project_config(
            host=existing_project.host, project_id=project_id
        )

        config.profiles[project] = updated_project
        validate_full_config_after_modification(config)

        save_config(config)
        logger.info(
            f"Updated project '{project}' with project_id {updated_project.project_id}"
        )

    except (ValidationError, ValueError) as e:
        logger.error(f"Failed to update project_id for project '{project}': {e}")
        raise


def delete_project_config(project: str) -> None:
    """
    Delete the configuration for a specific project.
    Args:
        project: dbt project name that is used to select the host and project_id
    """
    try:
        config = get_config()
        if not config:
            raise ValueError("Configuration file not found or invalid.")

        if project not in config.profiles:
            raise ValueError(f"Project '{project}' not found in configuration.")

        del config.profiles[project]

        validate_full_config_after_modification(config)

        save_config(config)
        logger.info(f"Deleted project '{project}'")

    except (ValidationError, ValueError) as e:
        logger.error(f"Failed to delete project '{project}': {e}")
        raise


def list_all_projects() -> None:
    """
    List all projects with their configuration details and mark the active one.
    Reads from dbt_switch.yml and cross-references with dbt_cloud.yml for active project.
    """
    from dbt_switch.config.cloud_handler import read_dbt_cloud_config

    config = get_config()
    if not config or not config.profiles:
        logger.info(
            "No projects configured. Run 'dbt-switch init' and 'dbt-switch add' to get started."
        )
        return

    cloud_config = read_dbt_cloud_config()
    active_project = None
    if cloud_config:
        for project_name, project_config in config.profiles.items():
            if (
                project_config.host == cloud_config.context.active_host
                and str(project_config.project_id)
                == cloud_config.context.active_project
            ):
                active_project = project_name
                break

    print("Available projects:")
    for project_name, project_config in config.profiles.items():
        active_marker = " [ACTIVE]" if project_name == active_project else ""
        prefix = "  * " if project_name == active_project else "    "
        print(
            f"{prefix}{project_name:<12} ({project_config.host}, ID: {project_config.project_id}){active_marker}"
        )
