from pathlib import Path
from .logger import logger

DIRECTORY = Path.home() / ".dbt"
CONFIG_FILE = DIRECTORY / "dbt_switch.yml"

def init_config():
    """
    Initialize the dbt_switch.yml file in the .dbt directory.
    This file contains the active project and host for the dbt Cloud project.
    """
    if not CONFIG_FILE.exists():
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.touch()
        logger.info(f"Initialized {CONFIG_FILE}")
    else:
        logger.info(f"{CONFIG_FILE} already exists")