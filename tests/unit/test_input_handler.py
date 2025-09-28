"""
Simplified unit tests for input handling operations.
"""

from unittest.mock import patch
from dbt_switch.config.input_handler import (
    add_user_config,
    update_user_config,
    delete_user_config,
    update_user_config_interactive,
    update_user_config_non_interactive,
)


class TestInputHandlers:
    """Test input handler functions."""

    @patch("dbt_switch.config.input_handler.add_config")
    @patch("builtins.input")
    def test_add_input_success(self, mock_input, mock_add_config):
        """Test successful input handling."""
        mock_input.side_effect = ["test-project", "test.getdbt.com", "12345"]

        add_user_config("add")

        mock_add_config.assert_called_once_with(
            "test-project", "test.getdbt.com", 12345
        )

    @patch("dbt_switch.config.input_handler.update_project")
    @patch("builtins.input")
    def test_update_input(self, mock_input, mock_update_host):
        """Test update input handling."""
        mock_input.side_effect = ["test-project", "new-host.getdbt.com"]

        update_user_config("host")

        mock_update_host.assert_called_once_with(
            "test-project", host="new-host.getdbt.com"
        )

    @patch("dbt_switch.config.input_handler.delete_project_config")
    @patch("builtins.input")
    def test_delete_input(self, mock_input, mock_delete):
        """Test delete input handling."""
        mock_input.return_value = "test-project"

        delete_user_config("delete")

        mock_delete.assert_called_once_with("test-project")

    @patch("dbt_switch.config.input_handler.update_project")
    @patch("builtins.input")
    def test_update_project_id_backward_compatibility(self, mock_input, mock_update_id):
        """Test backward compatibility for project_id update."""
        mock_input.side_effect = ["test-project", "54321"]

        update_user_config("project_id")

        mock_update_id.assert_called_once_with("test-project", project_id=54321)

    def test_import_new_functions(self):
        """Test that new functions can be imported without error."""
        # This test ensures the new functions are available and importable
        assert callable(update_user_config_interactive)
        assert callable(update_user_config_non_interactive)
