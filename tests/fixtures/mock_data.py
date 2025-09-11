"""
Mock data and utilities for dbt-switch tests.
"""

from typing import Dict, Any, List
from dbt_switch.validation.schemas import DbtSwitchConfig, ProjectConfig


class MockDataGenerator:
    """Generate mock data for testing."""

    @staticmethod
    def create_project_config(
        host: str = "test.getdbt.com", project_id: int = 12345
    ) -> ProjectConfig:
        """Create a mock ProjectConfig."""
        return ProjectConfig(host=host, project_id=project_id)

    @staticmethod
    def create_dbt_switch_config(
        profiles: Dict[str, ProjectConfig] = None,
    ) -> DbtSwitchConfig:
        """Create a mock DbtSwitchConfig."""
        if profiles is None:
            profiles = {"test-project": MockDataGenerator.create_project_config()}
        return DbtSwitchConfig(profiles=profiles)

    @staticmethod
    def create_multiple_projects(count: int = 3) -> Dict[str, ProjectConfig]:
        """Create multiple mock projects."""
        projects = {}
        for i in range(count):
            name = f"project-{i + 1}"
            host = f"project{i + 1}.getdbt.com"
            project_id = (i + 1) * 11111
            projects[name] = ProjectConfig(host=host, project_id=project_id)
        return projects

    @staticmethod
    def create_config_dict(
        profiles: Dict[str, Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a mock config dictionary."""
        if profiles is None:
            profiles = {
                "test-project": {"host": "test.getdbt.com", "project_id": 12345}
            }
        return {"profiles": profiles}

    @staticmethod
    def create_user_input_data(
        name: str = "test-project",
        host: str = "test.getdbt.com",
        project_id: int = 12345,
    ) -> Dict[str, Any]:
        """Create mock user input data."""
        return {"name": name, "host": host, "project_id": project_id}


class MockValidationScenarios:
    """Predefined validation test scenarios."""

    @staticmethod
    def get_valid_project_configs() -> List[Dict[str, Any]]:
        """Get list of valid project configurations."""
        return [
            {"host": "company.getdbt.com", "project_id": 12345},
            {"host": "prod-env.getdbt.com", "project_id": 99999},
            {"host": "dev.company.getdbt.com", "project_id": 11111},
            {"host": "staging-env.getdbt.com", "project_id": 55555},
        ]

    @staticmethod
    def get_invalid_project_configs() -> List[Dict[str, Any]]:
        """Get list of invalid project configurations."""
        return [
            {"host": "", "project_id": 12345},  # Empty host
            {"host": "   ", "project_id": 12345},  # Whitespace host
            {"host": "valid.getdbt.com", "project_id": 0},  # Zero project ID
            {"host": "valid.getdbt.com", "project_id": -1},  # Negative project ID
            {"host": "123", "project_id": 12345},  # Numeric host
            {"host": "123.456", "project_id": 12345},  # Numeric host with dots
        ]

    @staticmethod
    def get_valid_project_names() -> List[str]:
        """Get list of valid project names."""
        return [
            "production",
            "dev-env",
            "test_123",
            "STAGING",
            "project-1",
            "my_project",
            "Project-Test-123",
        ]

    @staticmethod
    def get_invalid_project_names() -> List[str]:
        """Get list of invalid project names."""
        return [
            "",  # Empty
            "   ",  # Whitespace only
            "project with spaces",  # Spaces
            "project@domain",  # Special characters
            "project.with.dots",  # Dots
            "project/slash",  # Slash
            "project\\backslash",  # Backslash
            "project#hash",  # Hash
            "project$dollar",  # Dollar sign
        ]

    @staticmethod
    def get_duplicate_scenarios() -> List[Dict[str, Any]]:
        """Get scenarios for testing duplicate validation."""
        return [
            {
                "profiles": {
                    "proj1": {"host": "host1.getdbt.com", "project_id": 11111},
                    "proj2": {
                        "host": "host2.getdbt.com",
                        "project_id": 11111,
                    },  # Duplicate ID
                }
            },
            {
                "profiles": {
                    "same-name": {"host": "host1.getdbt.com", "project_id": 11111},
                    "same-name": {  # noqa: F601
                        "host": "host2.getdbt.com",
                        "project_id": 22222,
                    },  # Duplicate name (dict key)
                }
            },
        ]


class MockFileContents:
    """Mock file contents for testing."""

    @staticmethod
    def get_valid_yaml_config() -> str:
        """Get valid YAML config content."""
        return """
profiles:
  production:
    host: prod.company.getdbt.com
    project_id: 11111
  development:
    host: dev.company.getdbt.com
    project_id: 22222
  staging:
    host: staging.company.getdbt.com
    project_id: 33333
"""

    @staticmethod
    def get_invalid_yaml_config() -> str:
        """Get invalid YAML config content."""
        return """
profiles:
  invalid-project:
    host: ""
    project_id: -1
  another-invalid:
    host: "123.456"
    project_id: 0
"""

    @staticmethod
    def get_malformed_yaml() -> str:
        """Get malformed YAML content."""
        return """
profiles:
  test:
    host: unclosed_quote"
    project_id: [invalid_list
missing_colon
  invalid indentation
"""

    @staticmethod
    def get_empty_config() -> str:
        """Get empty config content."""
        return "profiles: {}"

    @staticmethod
    def get_minimal_config() -> str:
        """Get minimal valid config."""
        return """
profiles:
  single-project:
    host: single.getdbt.com
    project_id: 12345
"""

    @staticmethod
    def get_complex_config() -> str:
        """Get complex config with many projects."""
        return """
profiles:
  prod-api:
    host: api-prod.company.getdbt.com
    project_id: 10001
  prod-web:
    host: web-prod.company.getdbt.com  
    project_id: 10002
  dev-api:
    host: api-dev.company.getdbt.com
    project_id: 20001
  dev-web:
    host: web-dev.company.getdbt.com
    project_id: 20002
  staging-api:
    host: api-staging.company.getdbt.com
    project_id: 30001
  staging-web:
    host: web-staging.company.getdbt.com
    project_id: 30002
  test-env:
    host: test.company.getdbt.com
    project_id: 40001
"""


class MockInteractions:
    """Mock user interactions for testing."""

    @staticmethod
    def get_add_project_sequence() -> List[str]:
        """Get input sequence for adding a project."""
        return [
            "new-project",  # Project name
            "new.getdbt.com",  # Host
            "99999",  # Project ID
        ]

    @staticmethod
    def get_add_project_with_retries() -> List[str]:
        """Get input sequence with validation retries."""
        return [
            "",  # Empty name (retry)
            "valid-project",  # Valid name
            "",  # Empty host (retry)
            "valid.getdbt.com",  # Valid host
            "not_a_number",  # Invalid project ID (retry)
            "12345",  # Valid project ID
        ]

    @staticmethod
    def get_update_host_sequence() -> List[str]:
        """Get input sequence for updating host."""
        return [
            "project-to-update",  # Project selection
            "updated-host.getdbt.com",  # New host
        ]

    @staticmethod
    def get_update_project_id_sequence() -> List[str]:
        """Get input sequence for updating project ID."""
        return [
            "project-to-update",  # Project selection
            "99999",  # New project ID
        ]

    @staticmethod
    def get_delete_project_sequence() -> List[str]:
        """Get input sequence for deleting project."""
        return [
            "project-to-delete",  # Project selection
        ]

    @staticmethod
    def get_invalid_selection_sequence() -> List[str]:
        """Get input sequence with invalid selections."""
        return [
            "nonexistent-project",  # Invalid selection (retry)
            "valid-project",  # Valid selection
        ]


class MockEnvironments:
    """Mock environment setups for testing."""

    @staticmethod
    def get_isolated_env_vars(
        temp_home: str, temp_config_path: str = None
    ) -> Dict[str, str]:
        """Get environment variables for isolated testing."""
        env_vars = {"HOME": temp_home}
        if temp_config_path:
            env_vars["DBT_SWITCH_CONFIG_PATH"] = temp_config_path
        return env_vars

    @staticmethod
    def get_readonly_env_scenario(readonly_home: str) -> Dict[str, str]:
        """Get environment for read-only permission testing."""
        return {"HOME": readonly_home}

    @staticmethod
    def get_no_home_env() -> Dict[str, str]:
        """Get environment without HOME variable."""
        return {}


class MockLogMessages:
    """Expected log messages for testing."""

    @staticmethod
    def get_init_success_messages() -> List[str]:
        """Get expected messages for successful init."""
        return [
            "Initialized empty config file",
            "Config file already exists",
        ]

    @staticmethod
    def get_add_success_messages() -> List[str]:
        """Get expected messages for successful add."""
        return [
            "Successfully added project",
            "Project added successfully",
        ]

    @staticmethod
    def get_validation_error_messages() -> List[str]:
        """Get expected validation error messages."""
        return [
            "Project ID must be a positive integer",
            "Host must be a non-empty string",
            "Project name contains invalid characters",
            "Each project must have a unique project ID",
        ]

    @staticmethod
    def get_user_error_messages() -> List[str]:
        """Get expected user error messages."""
        return [
            "Project name already exists",
            "Please enter a valid",
            "Invalid selection",
            "No projects configured",
        ]


# Convenience functions for quick access to common mock data
def mock_project() -> ProjectConfig:
    """Quick access to a basic mock project."""
    return MockDataGenerator.create_project_config()


def mock_config() -> DbtSwitchConfig:
    """Quick access to a basic mock config."""
    return MockDataGenerator.create_dbt_switch_config()


def mock_multiple_projects(count: int = 3) -> DbtSwitchConfig:
    """Quick access to a config with multiple projects."""
    profiles = MockDataGenerator.create_multiple_projects(count)
    return DbtSwitchConfig(profiles=profiles)


def mock_empty_config() -> DbtSwitchConfig:
    """Quick access to an empty config."""
    return DbtSwitchConfig(profiles={})
