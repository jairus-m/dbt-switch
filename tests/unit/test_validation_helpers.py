"""
Unit tests for validation helper functions.
"""

import pytest

from dbt_switch.validation.helpers import (
    validate_project_name_format,
    check_project_name_exists,
    validate_unique_project_id,
    validate_full_config_after_modification,
    create_validated_project_config,
)
from dbt_switch.validation.schemas import DbtSwitchConfig, ProjectConfig


class TestValidateProjectNameFormat:
    """Test project name format validation."""

    @pytest.mark.parametrize(
        "valid_name",
        ["project-1", "Project_2", "PROD", "a-b_c-d_e"],
    )
    def test_valid_project_names(self, valid_name):
        """Test valid project names pass validation."""
        validate_project_name_format(valid_name)

    @pytest.mark.parametrize(
        "invalid_name",
        ["", "   ", "project with spaces", "project@domain", "project.with.dots"],
    )
    def test_invalid_project_names(self, invalid_name):
        """Test invalid project names raise ValueError."""
        with pytest.raises(ValueError):
            validate_project_name_format(invalid_name)

    def test_project_name_existence(self):
        """Test project name checking."""
        config = DbtSwitchConfig(
            profiles={"existing": ProjectConfig(host="test.com", project_id=123)}
        )

        assert check_project_name_exists(config, "existing") is True
        assert check_project_name_exists(config, "nonexistent") is False

    def test_project_id_validation(self):
        """Test project ID uniqueness validation."""
        config = DbtSwitchConfig(
            profiles={
                "proj1": ProjectConfig(host="host1.com", project_id=111),
                "proj2": ProjectConfig(host="host2.com", project_id=222),
            }
        )

        validate_unique_project_id(config, 333)

        with pytest.raises(ValueError, match="already in use"):
            validate_unique_project_id(config, 111)

    def test_config_validation(self):
        """Test config validation."""
        config = DbtSwitchConfig(
            profiles={
                "proj1": ProjectConfig(host="host1.com", project_id=111),
                "proj2": ProjectConfig(host="host2.com", project_id=222),
            }
        )

        validate_full_config_after_modification(config)

    def test_project_config_creation(self):
        """Test project config creation."""
        config = create_validated_project_config("test.com", 123)

        assert isinstance(config, ProjectConfig)
        assert config.host == "test.com"
        assert config.project_id == 123
