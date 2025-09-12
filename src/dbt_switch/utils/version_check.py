"""
Version check.
"""

from importlib.metadata import version, PackageNotFoundError


def get_current_version() -> str:
    """
    Get the current installed version of dbt-switch.
    Returns:
        str: Current version or 'unknown' if not found
    """
    try:
        return version("dbt-switch")
    except PackageNotFoundError:
        return "unknown"
