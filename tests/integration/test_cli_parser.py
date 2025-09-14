"""
Integration tests for CLI argument parsing and command routing.
"""

import pytest
from unittest.mock import patch
from click.testing import CliRunner

from dbt_switch.cli.parser import cli


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
        runner = CliRunner()
        with patch(mock_path) as mock_func:
            result = runner.invoke(cli, [command])
            assert result.exit_code == 0
            if expected_call is None:
                mock_func.assert_called_once()
            else:
                mock_func.assert_called_once_with(expected_call)

    @patch("dbt_switch.cli.parser.update_user_config_input")
    def test_parser_update_commands(self, mock_update):
        """Test update command variants."""
        runner = CliRunner()

        # Test update --host option
        result = runner.invoke(cli, ["update", "--host"])
        assert result.exit_code == 0
        mock_update.assert_called_with("host")

        mock_update.reset_mock()

        # Test update --project-id option
        result = runner.invoke(cli, ["update", "--project-id"])
        assert result.exit_code == 0
        mock_update.assert_called_with("project_id")

        mock_update.reset_mock()

        # Test update with no options (should show error)
        result = runner.invoke(cli, ["update"])
        assert result.exit_code == 0  # Command succeeds but shows error message
        mock_update.assert_not_called()

        # Test update with both options (should show error)
        result = runner.invoke(cli, ["update", "--host", "--project-id"])
        assert result.exit_code == 0  # Command succeeds but shows error message
        mock_update.assert_not_called()

    def test_parser_edge_cases(self):
        """Test parser edge cases."""
        runner = CliRunner()

        # Test help
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "dbt Cloud project and host switcher" in result.output

        # Test invalid command
        result = runner.invoke(cli, ["invalid"])
        assert result.exit_code != 0

    def test_list_command_execution(self):
        """Test that list command executes without errors."""
        runner = CliRunner()
        with patch("dbt_switch.cli.parser.list_projects") as mock_list_projects:
            result = runner.invoke(cli, ["list"])
            assert result.exit_code == 0
            mock_list_projects.assert_called_once()

    def test_version_flag(self):
        """Test that --version flag works correctly."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "dbt-switch" in result.output
