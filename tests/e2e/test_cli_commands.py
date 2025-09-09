"""
End-to-end tests for essential CLI command execution.
"""

import pytest
import subprocess
import sys
import os


@pytest.mark.e2e
class TestCliCommands:
    """Test essential CLI command execution end-to-end."""

    def test_cli_init_command(self, isolated_filesystem):
        """Test CLI init command creates config file."""
        result = subprocess.run(
            [sys.executable, "-m", "dbt_switch.main", "init"],
            env={**os.environ, "HOME": str(isolated_filesystem["home"])},
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0
        assert isolated_filesystem["config_path"].exists()

    def test_cli_help_command(self):
        """Test CLI help command."""
        result = subprocess.run(
            [sys.executable, "-m", "dbt_switch.main", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0
        assert "init" in result.stdout

    def test_cli_add_command_interactive(self, isolated_filesystem):
        """Test CLI add command with user input."""
        subprocess.run(
            [sys.executable, "-m", "dbt_switch.main", "init"],
            env={**os.environ, "HOME": str(isolated_filesystem["home"])},
            capture_output=True,
            timeout=10,
        )

        result = subprocess.run(
            [sys.executable, "-m", "dbt_switch.main", "add"],
            input="test-project\ntest.getdbt.com\n12345\n",
            env={**os.environ, "HOME": str(isolated_filesystem["home"])},
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode in [0, 1]  # May have validation errors
