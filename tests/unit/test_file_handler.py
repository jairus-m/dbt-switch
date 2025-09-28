"""
Simplified unit tests for file handling operations.
"""

import pytest
from unittest.mock import patch, MagicMock

from dbt_switch.config.file_handler import (
    init_config,
    get_config,
    add_config,
    get_project_config,
    update_project,
    delete_project_config,
)
from dbt_switch.validation.schemas import DbtSwitchConfig, ProjectConfig


@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file path."""
    return tmp_path / "dbt_switch.yml"


class TestFileOperations:
    """Test core file operations."""

    @patch("dbt_switch.config.file_handler.CONFIG_FILE")
    def test_init_config(self, mock_config_file):
        """Test config initialization."""
        mock_config_file.exists.return_value = False
        mock_config_file.parent.mkdir = MagicMock()

        with patch("builtins.open", create=True), patch("yaml.dump"):
            init_config()

    @patch("dbt_switch.config.file_handler.CONFIG_FILE")
    def test_get_config(self, mock_config_file):
        """Test loading config."""
        mock_config_file.exists.return_value = True

        with patch("builtins.open", create=True):
            with patch("yaml.safe_load", return_value={"profiles": {}}):
                result = get_config()
                assert isinstance(result, DbtSwitchConfig)


class TestAddConfig:
    """Test adding configuration."""

    @patch("dbt_switch.config.file_handler.get_config")
    @patch("dbt_switch.config.file_handler.save_config")
    def test_add_config_to_empty(self, mock_save, mock_get):
        """Test adding config to empty configuration."""
        mock_get.return_value = DbtSwitchConfig(profiles={})

        add_config("test-project", "test.getdbt.com", 12345)

        mock_save.assert_called_once()
        saved_config = mock_save.call_args[0][0]
        assert "test-project" in saved_config.profiles
        assert saved_config.profiles["test-project"].host == "test.getdbt.com"
        assert saved_config.profiles["test-project"].project_id == 12345

    @patch("dbt_switch.config.file_handler.get_config")
    def test_add_config_validations(self, mock_get):
        """Test add config validation failures."""
        existing_config = DbtSwitchConfig(
            profiles={
                "existing": ProjectConfig(host="existing.getdbt.com", project_id=11111)
            }
        )
        mock_get.return_value = existing_config

        with pytest.raises(ValueError):
            add_config("existing", "new.getdbt.com", 22222)

    @patch("dbt_switch.config.file_handler.get_config")
    def test_get_project_config(self, mock_get):
        """Test getting project configuration."""
        config = DbtSwitchConfig(
            profiles={
                "test-project": ProjectConfig(host="test.getdbt.com", project_id=12345)
            }
        )
        mock_get.return_value = config

        result = get_project_config("test-project")
        assert result is not None
        assert result.host == "test.getdbt.com"

        result = get_project_config("nonexistent")
        assert result is None


class TestUpdateProject:
    """Test updating project configurations."""

    @patch("dbt_switch.config.file_handler.get_config")
    @patch("dbt_switch.config.file_handler.save_config")
    def test_update_existing_project_host(self, mock_save, mock_get):
        """Test updating existing project host."""
        config = DbtSwitchConfig(
            profiles={
                "test-project": ProjectConfig(host="old.getdbt.com", project_id=12345)
            }
        )
        mock_get.return_value = config

        update_project("test-project", host="new.getdbt.com")

        mock_save.assert_called_once()
        saved_config = mock_save.call_args[0][0]
        assert saved_config.profiles["test-project"].host == "new.getdbt.com"

    @patch("dbt_switch.config.file_handler.get_config")
    @patch("dbt_switch.config.file_handler.save_config")
    def test_update_existing_project_id(self, mock_save, mock_get):
        """Test updating existing project ID."""
        config = DbtSwitchConfig(
            profiles={
                "test-project": ProjectConfig(host="test.getdbt.com", project_id=12345)
            }
        )
        mock_get.return_value = config

        update_project("test-project", project_id=99999)

        mock_save.assert_called_once()
        saved_config = mock_save.call_args[0][0]
        assert saved_config.profiles["test-project"].project_id == 99999

    @patch("dbt_switch.config.file_handler.get_config")
    def test_update_nonexistent_project_fails(self, mock_get):
        """Test updating non-existent project fails."""
        config = DbtSwitchConfig(profiles={})
        mock_get.return_value = config

        with pytest.raises(ValueError):
            update_project("nonexistent", host="new.getdbt.com")

    @patch("dbt_switch.config.file_handler.get_config")
    def test_update_project_id_duplicate_fails(self, mock_get):
        """Test updating project ID to duplicate fails."""
        config = DbtSwitchConfig(
            profiles={
                "proj1": ProjectConfig(host="host1.getdbt.com", project_id=11111),
                "proj2": ProjectConfig(host="host2.getdbt.com", project_id=22222),
            }
        )
        mock_get.return_value = config

        with pytest.raises(ValueError):
            update_project("proj1", project_id=22222)


class TestDeleteProjectConfig:
    """Test deleting project configuration."""

    @patch("dbt_switch.config.file_handler.get_config")
    @patch("dbt_switch.config.file_handler.save_config")
    def test_delete_existing_project(self, mock_save, mock_get):
        """Test deleting existing project."""
        config = DbtSwitchConfig(
            profiles={
                "proj1": ProjectConfig(host="host1.getdbt.com", project_id=11111),
                "proj2": ProjectConfig(host="host2.getdbt.com", project_id=22222),
            }
        )
        mock_get.return_value = config

        delete_project_config("proj1")

        mock_save.assert_called_once()
        saved_config = mock_save.call_args[0][0]
        assert "proj1" not in saved_config.profiles
        assert "proj2" in saved_config.profiles

    @patch("dbt_switch.config.file_handler.get_config")
    def test_delete_nonexistent_project_fails(self, mock_get):
        """Test deleting non-existent project fails."""
        config = DbtSwitchConfig(profiles={})
        mock_get.return_value = config

        with pytest.raises(ValueError):
            delete_project_config("nonexistent")
