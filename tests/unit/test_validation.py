"""
Simplified unit tests for Pydantic validation models.
"""

import pytest
from pydantic import ValidationError

from dbt_switch.validation.schemas import ProjectConfig, DbtSwitchConfig


class TestProjectConfig:
    """Test cases for ProjectConfig validation."""

    def test_valid_project_config(self):
        """Test creating a valid ProjectConfig."""
        config = ProjectConfig(host="mycompany.getdbt.com", project_id=12345)
        assert config.host == "mycompany.getdbt.com"
        assert config.project_id == 12345

    @pytest.mark.parametrize("project_id", [-1, 0, -999])
    def test_invalid_project_id(self, project_id):
        """Test ProjectConfig rejects invalid project IDs."""
        with pytest.raises(ValidationError):
            ProjectConfig(host="valid.getdbt.com", project_id=project_id)

    @pytest.mark.parametrize("host", ["", "   "])
    def test_invalid_host_empty(self, host):
        """Test ProjectConfig rejects empty hosts."""
        with pytest.raises(ValidationError):
            ProjectConfig(host=host, project_id=12345)


class TestDbtSwitchConfig:
    """Test cases for DbtSwitchConfig validation."""

    def test_empty_config_valid(self):
        """Test that empty config is valid."""
        config = DbtSwitchConfig(profiles={})
        assert len(config.profiles) == 0

    def test_valid_config_with_projects(self):
        """Test valid config with projects."""
        config = DbtSwitchConfig(
            profiles={
                "prod": ProjectConfig(host="prod.getdbt.com", project_id=11111),
                "dev": ProjectConfig(host="dev.getdbt.com", project_id=22222),
            }
        )
        assert len(config.profiles) == 2
        assert "prod" in config.profiles
        assert "dev" in config.profiles

    def test_duplicate_project_ids_rejected(self):
        """Test that duplicate project IDs are rejected."""
        with pytest.raises(ValidationError):
            DbtSwitchConfig(
                profiles={
                    "proj1": ProjectConfig(host="host1.getdbt.com", project_id=12345),
                    "proj2": ProjectConfig(host="host2.getdbt.com", project_id=12345),
                }
            )
