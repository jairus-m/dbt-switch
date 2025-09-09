"""
Shared pytest fixtures and configuration for dbt-switch tests.
"""

import os
import pytest
from unittest.mock import patch

from dbt_switch.validation.schemas import DbtSwitchConfig, ProjectConfig


@pytest.fixture
def temp_home_dir(tmp_path):
    """Create a temporary home directory for testing."""
    home_dir = tmp_path / "home"
    home_dir.mkdir()
    return home_dir


@pytest.fixture
def temp_dbt_dir(temp_home_dir):
    """Create a temporary .dbt directory."""
    dbt_dir = temp_home_dir / ".dbt"
    dbt_dir.mkdir()
    return dbt_dir


@pytest.fixture
def temp_config_file(temp_dbt_dir):
    """Create a temporary config file path."""
    return temp_dbt_dir / "dbt_switch.yml"


@pytest.fixture
def mock_home_env(temp_home_dir, monkeypatch):
    """Mock the HOME environment variable to use temp directory."""
    monkeypatch.setenv("HOME", str(temp_home_dir))
    return temp_home_dir


@pytest.fixture
def sample_project_config():
    """Return a sample ProjectConfig instance."""
    return ProjectConfig(host="mycompany.getdbt.com", project_id=12345)


@pytest.fixture
def sample_dbt_config():
    """Return a sample DbtSwitchConfig instance."""
    return DbtSwitchConfig(
        profiles={
            "prod": ProjectConfig(host="prod.getdbt.com", project_id=11111),
            "dev": ProjectConfig(host="dev.getdbt.com", project_id=22222),
            "staging": ProjectConfig(host="staging.getdbt.com", project_id=33333),
        }
    )


@pytest.fixture
def sample_config_dict():
    """Return a sample config as a dictionary."""
    return {
        "profiles": {
            "prod": {"host": "prod.getdbt.com", "project_id": 11111},
            "dev": {"host": "dev.getdbt.com", "project_id": 22222},
            "staging": {"host": "staging.getdbt.com", "project_id": 33333},
        }
    }


@pytest.fixture
def valid_config_yaml():
    """Return valid config as YAML string."""
    return """
profiles:
  prod:
    host: prod.getdbt.com
    project_id: 11111
  dev:
    host: dev.getdbt.com
    project_id: 22222
"""


@pytest.fixture
def invalid_config_yaml():
    """Return invalid config as YAML string."""
    return """
profiles:
  prod:
    host: ""
    project_id: -1
  dev:
    host: dev.getdbt.com
    project_id: "not_a_number"
"""


@pytest.fixture
def empty_config_yaml():
    """Return minimal empty config."""
    return "profiles: {}"


@pytest.fixture
def config_file_with_content(temp_config_file, valid_config_yaml):
    """Create a config file with valid content."""
    temp_config_file.write_text(valid_config_yaml)
    return temp_config_file


@pytest.fixture
def mock_user_input():
    """Mock user input for interactive tests."""

    def _mock_input(inputs):
        input_iter = iter(inputs)
        return lambda _: next(input_iter)

    return _mock_input


@pytest.fixture
def mock_logger():
    """Mock the logger to capture log messages."""
    with patch("dbt_switch.utils.logger.logger") as mock_log:
        yield mock_log


@pytest.fixture
def cli_runner():
    """Pytest fixture for CLI testing."""
    import subprocess
    import sys

    def _run_cli(*args):
        """Run the CLI with given arguments."""
        cmd = [sys.executable, "-m", "dbt_switch.main"] + list(args)
        return subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    return _run_cli


@pytest.fixture(
    params=[
        {"host": "valid.getdbt.com", "project_id": 12345},
        {"host": "another.getdbt.com", "project_id": 67890},
    ]
)
def valid_project_data(request):
    """Parameterized fixture for valid project configurations."""
    return request.param


@pytest.fixture(
    params=[
        {"host": "", "project_id": 12345},
        {"host": "valid.getdbt.com", "project_id": -1},
        {"host": "valid.getdbt.com", "project_id": 0},
        {"host": "123.456", "project_id": 12345},
        {"host": "123", "project_id": 12345},
    ]
)
def invalid_project_data(request):
    """Parameterized fixture for invalid project configurations."""
    return request.param


@pytest.fixture(
    params=["project-1", "project_2", "Project3", "PROD", "dev-env", "test_123"]
)
def valid_project_names(request):
    """Parameterized fixture for valid project names."""
    return request.param


@pytest.fixture(
    params=[
        "",
        "   ",
        "project with spaces",
        "project@domain",
        "project.with.dots",
        "project/slash",
        "project\\backslash",
    ]
)
def invalid_project_names(request):
    """Parameterized fixture for invalid project names."""
    return request.param


@pytest.fixture
def isolated_filesystem(tmp_path, monkeypatch):
    """
    Create an isolated filesystem for testing that doesn't interfere with real configs.
    """
    # Create a temporary directory structure
    fake_home = tmp_path / "fake_home"
    fake_home.mkdir()
    fake_dbt = fake_home / ".dbt"
    fake_dbt.mkdir()

    # Mock environment variables
    monkeypatch.setenv("HOME", str(fake_home))
    monkeypatch.setenv("DBT_SWITCH_CONFIG_PATH", str(fake_dbt / "dbt_switch.yml"))

    # Change to temp directory
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    yield {
        "home": fake_home,
        "dbt_dir": fake_dbt,
        "config_path": fake_dbt / "dbt_switch.yml",
    }

    # Cleanup
    os.chdir(original_cwd)


@pytest.fixture
def capture_output():
    """Fixture to capture stdout/stderr during tests."""
    import io
    import contextlib

    @contextlib.contextmanager
    def _capture():
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            yield {"stdout": stdout, "stderr": stderr}

    return _capture


# Test configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "e2e: mark test as an end-to-end test")
    config.addinivalue_line("markers", "slow: mark test as slow running")


# Pytest collection hooks
def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their location."""
    for item in items:
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
            item.add_marker(pytest.mark.slow)
