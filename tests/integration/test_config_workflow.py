"""
Integration tests for complete config management workflows.
"""

from unittest.mock import patch, MagicMock

from dbt_switch.config.file_handler import (
    init_config,
    add_config,
    update_project_host,
    update_project_id,
    delete_project_config,
)
from dbt_switch.config.input_handler import (
    add_user_config_input,
    switch_user_config_input,
)
from dbt_switch.validation.schemas import DbtSwitchConfig, ProjectConfig


class TestConfigWorkflows:
    """Test config management workflows."""

    @patch("dbt_switch.config.file_handler.CONFIG_FILE")
    def test_init_config_workflow(self, mock_config_file):
        """Test config initialization."""
        mock_config_file.exists.return_value = False
        mock_config_file.parent.mkdir = MagicMock()

        with patch("builtins.open", create=True), patch("yaml.dump"):
            init_config()

    @patch("dbt_switch.config.file_handler.get_config")
    @patch("dbt_switch.config.file_handler.save_config")
    def test_add_project_workflow(self, mock_save, mock_get):
        """Test adding projects workflow."""
        mock_get.return_value = DbtSwitchConfig(profiles={})

        add_config("test-project", "test.getdbt.com", 12345)

        mock_save.assert_called_once()
        saved_config = mock_save.call_args[0][0]
        assert "test-project" in saved_config.profiles

    @patch("dbt_switch.config.file_handler.get_config")
    @patch("dbt_switch.config.file_handler.save_config")
    def test_update_workflows(self, mock_save, mock_get):
        """Test update workflows."""
        config = DbtSwitchConfig(
            profiles={"proj1": ProjectConfig(host="old.getdbt.com", project_id=11111)}
        )
        mock_get.return_value = config

        update_project_host("proj1", "new.getdbt.com")
        mock_save.assert_called()

        update_project_id("proj1", 99999)
        assert mock_save.call_count == 2

    @patch("dbt_switch.config.file_handler.get_config")
    @patch("dbt_switch.config.file_handler.save_config")
    def test_delete_workflow(self, mock_save, mock_get):
        """Test delete project workflow."""
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

    @patch("dbt_switch.config.input_handler.add_config")
    @patch("builtins.input")
    def test_input_handler_workflow(self, mock_input, mock_add_config):
        """Test input handler workflow."""
        mock_input.side_effect = ["test-project", "test.getdbt.com", "12345"]

        add_user_config_input("add")

        mock_add_config.assert_called_once_with(
            "test-project", "test.getdbt.com", 12345
        )

    @patch("dbt_switch.config.input_handler.switch_project")
    def test_switch_workflow(self, mock_switch):
        """Test switch project workflow."""
        switch_user_config_input("test-project")

        mock_switch.assert_called_once_with("test-project")
