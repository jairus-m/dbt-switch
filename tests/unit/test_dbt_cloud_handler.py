"""
Unit tests for cloud_handler module.
"""

import pytest
from unittest.mock import patch, mock_open

from dbt_switch.config.cloud_handler import (
    read_dbt_cloud_config,
    update_dbt_cloud_config,
    switch_project,
)
from dbt_switch.validation.schemas import DbtCloudConfig, DbtCloudContext


class TestReadDbtCloudConfig:
    @patch("dbt_switch.config.cloud_handler.DBT_CLOUD_FILE")
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.safe_load")
    def test_read_valid_config(self, mock_yaml_load, mock_file, mock_path):
        mock_path.exists.return_value = True
        mock_yaml_load.return_value = {
            "version": "1",
            "context": {"active-host": "test.com", "active-project": "12345"},
            "projects": [],
        }

        result = read_dbt_cloud_config()

        assert result is not None
        assert result.version == "1"
        assert result.context.active_host == "test.com"
        assert result.context.active_project == "12345"

    @patch("dbt_switch.config.cloud_handler.DBT_CLOUD_FILE")
    def test_read_nonexistent_file(self, mock_path):
        mock_path.exists.return_value = False

        result = read_dbt_cloud_config()

        assert result is None


class TestUpdateDbtCloudConfig:
    def test_update_config(self):
        config = DbtCloudConfig(
            version="1",
            context=DbtCloudContext(active_host="old.com", active_project="67890"),
            projects=[],
        )

        updated = update_dbt_cloud_config(config, "new.com", "12345")

        assert updated.context.active_host == "new.com"
        assert updated.context.active_project == "12345"
        assert updated.version == "1"


class TestSwitchProject:
    @patch("dbt_switch.config.cloud_handler.get_project_config")
    @patch("dbt_switch.config.cloud_handler.read_dbt_cloud_config")
    @patch("dbt_switch.config.cloud_handler.write_dbt_cloud_config")
    def test_switch_project_success(self, mock_write, mock_read, mock_get_config):
        from dbt_switch.validation.schemas import ProjectConfig

        mock_get_config.return_value = ProjectConfig(host="test.com", project_id=12345)
        mock_read.return_value = DbtCloudConfig(
            version="1",
            context=DbtCloudContext(active_host="old.com", active_project="67890"),
            projects=[],
        )

        switch_project("test_project")

        mock_get_config.assert_called_once_with("test_project")
        mock_read.assert_called_once()
        mock_write.assert_called_once()

        # Check the written config
        written_config = mock_write.call_args[0][0]
        assert written_config.context.active_host == "test.com"
        assert written_config.context.active_project == "12345"

    @patch("dbt_switch.config.cloud_handler.get_project_config")
    def test_switch_project_not_found(self, mock_get_config):
        mock_get_config.return_value = None

        with pytest.raises(ValueError, match="Project 'nonexistent' not found"):
            switch_project("nonexistent")
