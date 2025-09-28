"""
Comprehensive unit tests for the new interactive update functionality.
"""

from unittest.mock import patch, MagicMock
import pytest
from dbt_switch.config.input_handler import (
    update_user_config_interactive,
    update_user_config_non_interactive,
)
from dbt_switch.config.file_handler import (
    update_project,
    display_project_config,
)


class TestInteractiveUpdate:
    """Test interactive update functionality."""

    @patch("dbt_switch.config.input_handler.display_project_config")
    @patch("dbt_switch.config.input_handler.update_project")
    @patch("builtins.input")
    def test_interactive_update_host_only(
        self, mock_input, mock_update_host, mock_display
    ):
        """Test interactive update of host only."""
        mock_input.side_effect = ["1", "new-host.getdbt.com"]

        update_user_config_interactive("test-project")

        mock_display.assert_called_once_with("test-project")
        mock_update_host.assert_called_once_with(
            "test-project", host="new-host.getdbt.com"
        )

    @patch("dbt_switch.config.input_handler.display_project_config")
    @patch("dbt_switch.config.input_handler.update_project")
    @patch("builtins.input")
    def test_interactive_update_project_id_only(
        self, mock_input, mock_update_id, mock_display
    ):
        """Test interactive update of project ID only."""
        mock_input.side_effect = ["2", "67890"]

        update_user_config_interactive("test-project")

        mock_display.assert_called_once_with("test-project")
        mock_update_id.assert_called_once_with("test-project", project_id=67890)

    @patch("dbt_switch.config.input_handler.display_project_config")
    @patch("dbt_switch.config.input_handler.update_project")
    @patch("builtins.input")
    def test_interactive_update_both(self, mock_input, mock_update_both, mock_display):
        """Test interactive update of both host and project ID."""
        mock_input.side_effect = ["3", "new-host.getdbt.com", "67890"]

        update_user_config_interactive("test-project")

        mock_display.assert_called_once_with("test-project")
        mock_update_both.assert_called_once_with(
            "test-project", host="new-host.getdbt.com", project_id=67890
        )

    @patch("dbt_switch.config.input_handler.display_project_config")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_update_quit(self, mock_print, mock_input, mock_display):
        """Test interactive update quit option."""
        mock_input.return_value = "q"

        update_user_config_interactive("test-project")

        mock_display.assert_called_once_with("test-project")
        mock_print.assert_any_call("Update cancelled.")

    @patch("dbt_switch.config.input_handler.display_project_config")
    @patch("builtins.input")
    @patch("dbt_switch.utils.logger.logger.error")
    def test_interactive_update_invalid_choice(
        self, mock_logger, mock_input, mock_display
    ):
        """Test interactive update with invalid choice."""
        mock_input.return_value = "5"

        update_user_config_interactive("test-project")

        mock_display.assert_called_once_with("test-project")
        mock_logger.assert_called_with("Invalid choice. Please select 1, 2, 3, or q.")

    @patch("dbt_switch.utils.logger.logger.error")
    def test_interactive_update_empty_project_name(self, mock_logger):
        """Test interactive update with empty project name."""
        update_user_config_interactive("")

        mock_logger.assert_called_with("Project name cannot be empty")

    @patch("dbt_switch.config.input_handler.display_project_config")
    @patch("builtins.input")
    @patch("dbt_switch.utils.logger.logger.error")
    def test_interactive_update_empty_host(self, mock_logger, mock_input, mock_display):
        """Test interactive update with empty host input."""
        mock_input.side_effect = ["1", ""]

        update_user_config_interactive("test-project")

        mock_display.assert_called_once_with("test-project")
        mock_logger.assert_called_with("Project host cannot be empty")

    @patch("dbt_switch.config.input_handler.display_project_config")
    @patch("builtins.input")
    @patch("dbt_switch.utils.logger.logger.error")
    def test_interactive_update_invalid_project_id(
        self, mock_logger, mock_input, mock_display
    ):
        """Test interactive update with invalid project ID."""
        mock_input.side_effect = ["2", "not-a-number"]

        update_user_config_interactive("test-project")

        mock_display.assert_called_once_with("test-project")
        mock_logger.assert_called_with(
            "Invalid project ID 'not-a-number': must be a number"
        )


class TestNonInteractiveUpdate:
    """Test non-interactive update functionality."""

    @patch("dbt_switch.config.input_handler.update_project")
    def test_non_interactive_update_both(self, mock_update_both):
        """Test non-interactive update of both host and project ID."""
        update_user_config_non_interactive("test-project", "new-host.getdbt.com", 67890)

        mock_update_both.assert_called_once_with(
            "test-project", host="new-host.getdbt.com", project_id=67890
        )

    @patch("dbt_switch.config.input_handler.update_project")
    def test_non_interactive_update_host_only(self, mock_update_host):
        """Test non-interactive update of host only."""
        update_user_config_non_interactive("test-project", "new-host.getdbt.com", None)

        mock_update_host.assert_called_once_with(
            "test-project", host="new-host.getdbt.com"
        )

    @patch("dbt_switch.config.input_handler.update_project")
    def test_non_interactive_update_project_id_only(self, mock_update_id):
        """Test non-interactive update of project ID only."""
        update_user_config_non_interactive("test-project", None, 67890)

        mock_update_id.assert_called_once_with("test-project", project_id=67890)

    @patch("dbt_switch.utils.logger.logger.error")
    def test_non_interactive_update_empty_project_name(self, mock_logger):
        """Test non-interactive update with empty project name."""
        update_user_config_non_interactive("", "host", 123)

        mock_logger.assert_called_with("Project name cannot be empty")

    @patch("dbt_switch.utils.logger.logger.error")
    def test_non_interactive_update_empty_host(self, mock_logger):
        """Test non-interactive update with empty host."""
        update_user_config_non_interactive("test-project", "", 123)

        mock_logger.assert_called_with("Project host cannot be empty")

    @patch("dbt_switch.utils.logger.logger.error")
    def test_non_interactive_update_no_parameters(self, mock_logger):
        """Test non-interactive update with no host or project ID."""
        update_user_config_non_interactive("test-project", None, None)

        mock_logger.assert_called_with("Must specify either host, project_id, or both")


class TestUpdateProject:
    """Test update_project function."""

    @patch("dbt_switch.config.file_handler.save_config")
    @patch("dbt_switch.config.file_handler.validate_full_config_after_modification")
    @patch("dbt_switch.config.file_handler.create_validated_project_config")
    @patch("dbt_switch.config.file_handler.validate_unique_project_id")
    @patch("dbt_switch.config.file_handler.get_config")
    @patch("dbt_switch.utils.logger.logger.info")
    def test_update_project_success(
        self,
        mock_logger,
        mock_get_config,
        mock_validate_id,
        mock_create_project,
        mock_validate_config,
        mock_save_config,
    ):
        """Test successful update of both host and project ID."""
        # Mock config
        mock_config = MagicMock()
        mock_config.profiles = {"test-project": MagicMock()}
        mock_get_config.return_value = mock_config

        # Mock validated project
        mock_project = MagicMock()
        mock_project.host = "new-host.getdbt.com"
        mock_project.project_id = 67890
        mock_create_project.return_value = mock_project

        update_project("test-project", host="new-host.getdbt.com", project_id=67890)

        mock_validate_id.assert_called_once_with(
            mock_config, 67890, exclude_project="test-project"
        )
        mock_create_project.assert_called_once_with(
            host="new-host.getdbt.com", project_id=67890
        )
        mock_validate_config.assert_called_once_with(mock_config)
        mock_save_config.assert_called_once_with(mock_config)
        mock_logger.assert_called_with(
            "Updated project 'test-project' with host 'new-host.getdbt.com' and project_id 67890"
        )

    @patch("dbt_switch.config.file_handler.get_config")
    @patch("dbt_switch.utils.logger.logger.error")
    def test_update_project_no_config(self, mock_logger, mock_get_config):
        """Test update_project with no config file."""
        mock_get_config.return_value = None

        with pytest.raises(ValueError):
            update_project("test-project", host="host", project_id=123)

        mock_logger.assert_called_with(
            "Failed to update project 'test-project': Configuration file not found or invalid."
        )

    @patch("dbt_switch.config.file_handler.get_config")
    @patch("dbt_switch.utils.logger.logger.error")
    def test_update_project_project_not_found(self, mock_logger, mock_get_config):
        """Test update_project with project not found."""
        mock_config = MagicMock()
        mock_config.profiles = {}
        mock_get_config.return_value = mock_config

        with pytest.raises(ValueError):
            update_project("nonexistent-project", host="host", project_id=123)

        mock_logger.assert_called_with(
            "Failed to update project 'nonexistent-project': Project 'nonexistent-project' not found in configuration."
        )


class TestDisplayProjectConfig:
    """Test display_project_config function."""

    @patch("dbt_switch.config.file_handler.get_config")
    @patch("builtins.print")
    def test_display_project_config_success(self, mock_print, mock_get_config):
        """Test successful display of project configuration."""
        # Mock config
        mock_project = MagicMock()
        mock_project.host = "cloud.getdbt.com"
        mock_project.project_id = 12345

        mock_config = MagicMock()
        mock_config.profiles = {"test-project": mock_project}
        mock_get_config.return_value = mock_config

        display_project_config("test-project")

        mock_print.assert_any_call("\nCurrent configuration for 'test-project':")
        mock_print.assert_any_call("  Host:       cloud.getdbt.com")
        mock_print.assert_any_call("  Project ID: 12345")
        mock_print.assert_any_call()

    @patch("dbt_switch.config.file_handler.get_config")
    @patch("dbt_switch.utils.logger.logger.error")
    def test_display_project_config_no_config(self, mock_logger, mock_get_config):
        """Test display with no config file."""
        mock_get_config.return_value = None

        display_project_config("test-project")

        mock_logger.assert_called_with("Configuration file not found or invalid.")

    @patch("dbt_switch.config.file_handler.get_config")
    @patch("dbt_switch.utils.logger.logger.error")
    def test_display_project_config_project_not_found(
        self, mock_logger, mock_get_config
    ):
        """Test display with project not found."""
        mock_config = MagicMock()
        mock_config.profiles = {}
        mock_get_config.return_value = mock_config

        display_project_config("nonexistent-project")

        mock_logger.assert_called_with(
            "Project 'nonexistent-project' not found in configuration."
        )
