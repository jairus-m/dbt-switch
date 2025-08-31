from pathlib import Path
import yaml
from .logger import logger

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


def get_config() -> dict | None:
    """
    Get the config from the dbt_switch.yml file in the ~/.dbt directory.
    """
    if not CONFIG_FILE.exists():
        logger.info(f"{CONFIG_FILE} does not exist")
        return None
    with open(CONFIG_FILE, "r") as file:
        return yaml.safe_load(file)


def add_config(project: str, host: str, project_id: int) -> None:
    """
    Add a project configuration to the dbt_switch.yml file.
    Each project has a host and project_id.
    """
    config = get_config()
    if config is None:
        config = {"profiles": {}}

    if "profiles" not in config:
        config["profiles"] = {}

    # Add/update project configuration
    config["profiles"][project] = {"host": host, "project_id": project_id}

    with open(CONFIG_FILE, "w") as file:
        yaml.dump(config, file)

    logger.info(
        f"Added project '{project}' with host '{host}' and project_id {project_id}"
    )


def get_project_config(project: str) -> dict | None:
    """
    Get configuration for a specific project.
    Returns dict with 'host' and 'project_id' or None if not found.
    """
    config = get_config()
    if config and "profiles" in config and project in config["profiles"]:
        return config["profiles"][project]
    else:
        logger.error(f"Project '{project}' not found in configuration")
    return None


def update_project_host(project: str, host: str) -> None:
    """
    Update the configuration for a specific project.
    """
    config = get_config()
    if config and "profiles" in config and project in config["profiles"]:
        config["profiles"][project] = {"host": host}
        with open(CONFIG_FILE, "w") as file:
            yaml.dump(config, file)
        logger.info(f"Updated project '{project}' with host '{host}'")
    else:
        logger.error(f"Project '{project}' not found in configuration")


def update_project_id(project: str, project_id: int) -> None:
    """
    Update the configuration for a specific project.
    """
    config = get_config()
    if config and "profiles" in config and project in config["profiles"]:
        config["profiles"][project] = {"project_id": project_id}
        with open(CONFIG_FILE, "w") as file:
            yaml.dump(config, file)
        logger.info(f"Updated project '{project}' with project_id {project_id}")
    else:
        logger.error(f"Project '{project}' not found in configuration")


def delete_project_config(project: str) -> None:
    """
    Delete the configuration for a specific project.
    """
    config = get_config()
    if config and "profiles" in config and project in config["profiles"]:
        del config["profiles"][project]
        with open(CONFIG_FILE, "w") as file:
            yaml.dump(config, file)
        logger.info(f"Deleted project '{project}'")
    else:
        logger.error(f"Project '{project}' not found in configuration")
