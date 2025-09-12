"""
Integration tests for CLI argument parsing and command routing.
"""

import pytest
from unittest.mock import patch
import sys

from dbt_switch.cli.parser import arg_parser


class TestCliParser:
    """Test CLI argument parsing functionality."""

    @pytest.mark.parametrize(
        "command,mock_path,expected_call",
        [
            ("init", "dbt_switch.cli.parser.init_config", None),
            ("add", "dbt_switch.cli.parser.add_user_config_input", "add"),
            ("list", "dbt_switch.cli.parser.list_projects", None),
            ("delete", "dbt_switch.cli.parser.delete_user_config_input", "delete"),
        ],
    )
    def test_parser_commands(self, command, mock_path, expected_call):
        """Test basic command parsing."""
        with patch(mock_path) as mock_func:
            with patch.object(sys, "argv", ["dbt-switch", command]):
                arg_parser()
                if expected_call is None:
                    mock_func.assert_called_once()
                else:
                    mock_func.assert_called_once_with(expected_call)

    @patch("dbt_switch.cli.parser.update_user_config_input")
    def test_parser_update_commands(self, mock_update):
        """Test update command variants."""
        # Test --host flag
        with patch.object(sys, "argv", ["dbt-switch", "update", "--host"]):
            arg_parser()
            mock_update.assert_called_with("host")

        # Test --project-id flag
        with patch.object(sys, "argv", ["dbt-switch", "update", "--project-id"]):
            arg_parser()
            mock_update.assert_called_with("project_id")

    def test_parser_edge_cases(self):
        """Test parser edge cases."""
        # Test help
        with patch.object(sys, "argv", ["dbt-switch", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                arg_parser()
            assert exc_info.value.code == 0

        # Test invalid command
        with patch.object(sys, "argv", ["dbt-switch", "invalid"]):
            with pytest.raises(SystemExit) as exc_info:
                arg_parser()
            assert exc_info.value.code != 0

    def test_list_command_execution(self):
        """Test that list command executes without errors."""
        with patch("dbt_switch.cli.parser.list_projects") as mock_list_projects:
            with patch.object(sys, "argv", ["dbt-switch", "list"]):
                arg_parser()
                mock_list_projects.assert_called_once()

    def test_version_flag(self):
        """Test that --version flag works correctly."""
        with patch.object(sys, "argv", ["dbt-switch", "--version"]):
            with pytest.raises(SystemExit) as exc_info:
                arg_parser()
            assert exc_info.value.code == 0
