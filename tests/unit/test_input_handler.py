"""
Simplified unit tests for input handling operations.
"""

from unittest.mock import patch
from dbt_switch.config.input_handler import (
    add_user_config_input,
    update_user_config_input,
    delete_user_config_input,
)


class TestInputHandlers:
    """Test input handler functions."""

    @patch("dbt_switch.config.input_handler.add_config")
    @patch("builtins.input")
    def test_add_input_success(self, mock_input, mock_add_config):
        """Test successful input handling."""
        mock_input.side_effect = ["test-project", "test.getdbt.com", "12345"]

        add_user_config_input("add")

        mock_add_config.assert_called_once_with(
            "test-project", "test.getdbt.com", 12345
        )

    @patch("dbt_switch.config.input_handler.update_project_host")
    @patch("builtins.input")
    def test_update_input(self, mock_input, mock_update_host):
        """Test update input handling."""
        mock_input.side_effect = ["test-project", "new-host.getdbt.com"]

        update_user_config_input("host")

        mock_update_host.assert_called_once_with("test-project", "new-host.getdbt.com")

    @patch("dbt_switch.config.input_handler.delete_project_config")
    @patch("builtins.input")
    def test_delete_input(self, mock_input, mock_delete):
        """Test delete input handling."""
        mock_input.return_value = "test-project"

        delete_user_config_input("delete")

        mock_delete.assert_called_once_with("test-project")
