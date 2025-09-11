"""Unit tests for the list command functionality."""

from unittest.mock import patch, MagicMock
from dbt_switch.config.file_handler import list_all_projects
from dbt_switch.config.input_handler import list_projects
from dbt_switch.validation.schemas import (
    DbtSwitchConfig,
    ProjectConfig,
    DbtCloudConfig,
    DbtCloudContext,
)


def test_list_all_projects_empty_config():
    """Test list command with no projects configured."""
    with (
        patch("dbt_switch.config.file_handler.get_config") as mock_get_config,
        patch("dbt_switch.utils.logger.logger.info") as mock_logger_info,
    ):
        # Test with None config
        mock_get_config.return_value = None
        list_all_projects()
        mock_logger_info.assert_called_with(
            "No projects configured. Run 'dbt-switch init' and 'dbt-switch add' to get started."
        )

        # Test with empty profiles
        mock_config = MagicMock()
        mock_config.profiles = {}
        mock_get_config.return_value = mock_config
        list_all_projects()
        mock_logger_info.assert_called_with(
            "No projects configured. Run 'dbt-switch init' and 'dbt-switch add' to get started."
        )


def test_list_all_projects_with_active():
    """Test list command with projects and active project identified."""
    with (
        patch("dbt_switch.config.file_handler.get_config") as mock_get_config,
        patch(
            "dbt_switch.config.cloud_handler.read_dbt_cloud_config"
        ) as mock_read_dbt_cloud_config,
        patch("builtins.print") as mock_print,
    ):
        # Setup mock data
        mock_project_config1 = ProjectConfig(host="cloud.getdbt.com", project_id=12345)
        mock_project_config2 = ProjectConfig(host="cloud.getdbt.com", project_id=67890)

        mock_config = DbtSwitchConfig(
            profiles={"prod": mock_project_config1, "staging": mock_project_config2}
        )
        mock_get_config.return_value = mock_config

        # Setup cloud config with active project
        mock_cloud_config = DbtCloudConfig(
            version="1",
            context=DbtCloudContext(
                active_host="cloud.getdbt.com", active_project="12345"
            ),
        )
        mock_read_dbt_cloud_config.return_value = mock_cloud_config

        list_all_projects()

        # Verify the output
        mock_print.assert_any_call("Available projects:")
        mock_print.assert_any_call(
            "  * prod         (cloud.getdbt.com, ID: 12345) [ACTIVE]"
        )
        mock_print.assert_any_call("    staging      (cloud.getdbt.com, ID: 67890)")


def test_list_all_projects_no_active():
    """Test list command when no active project can be determined."""
    with (
        patch("dbt_switch.config.file_handler.get_config") as mock_get_config,
        patch(
            "dbt_switch.config.cloud_handler.read_dbt_cloud_config"
        ) as mock_read_dbt_cloud_config,
        patch("builtins.print") as mock_print,
    ):
        # Setup mock data
        mock_project_config1 = ProjectConfig(host="cloud.getdbt.com", project_id=12345)
        mock_project_config2 = ProjectConfig(
            host="partner.getdbt.com", project_id=54321
        )

        mock_config = DbtSwitchConfig(
            profiles={"prod": mock_project_config1, "dev": mock_project_config2}
        )
        mock_get_config.return_value = mock_config

        # Setup cloud config that doesn't match any project
        mock_cloud_config = DbtCloudConfig(
            version="1",
            context=DbtCloudContext(
                active_host="different.getdbt.com", active_project="99999"
            ),
        )
        mock_read_dbt_cloud_config.return_value = mock_cloud_config

        list_all_projects()

        # Verify the output shows no active project
        mock_print.assert_any_call("Available projects:")
        mock_print.assert_any_call("    prod         (cloud.getdbt.com, ID: 12345)")
        mock_print.assert_any_call("    dev          (partner.getdbt.com, ID: 54321)")


def test_list_all_projects_no_cloud_config():
    """Test list command when dbt_cloud.yml doesn't exist."""
    with (
        patch("dbt_switch.config.file_handler.get_config") as mock_get_config,
        patch(
            "dbt_switch.config.cloud_handler.read_dbt_cloud_config"
        ) as mock_read_dbt_cloud_config,
        patch("builtins.print") as mock_print,
    ):
        # Setup mock data
        mock_project_config1 = ProjectConfig(host="cloud.getdbt.com", project_id=12345)

        mock_config = DbtSwitchConfig(profiles={"prod": mock_project_config1})
        mock_get_config.return_value = mock_config

        # Cloud config returns None (file doesn't exist)
        mock_read_dbt_cloud_config.return_value = None

        list_all_projects()

        # Verify the output shows no active project
        mock_print.assert_any_call("Available projects:")
        mock_print.assert_any_call("    prod         (cloud.getdbt.com, ID: 12345)")


def test_list_projects_wrapper():
    """Test that the wrapper function calls the main function."""
    with patch(
        "dbt_switch.config.input_handler.list_all_projects"
    ) as mock_list_all_projects:
        list_projects()
        mock_list_all_projects.assert_called_once()
