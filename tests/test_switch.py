import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import sys
import io


from src.dbt_switch.main import switch_active_property, list_available_options, main

class TestDbtSwitch(unittest.TestCase):

    def setUp(self):
        self.mock_yaml_content = """version: "1"
context:
  active-host: "cloud.getdbt.com" # prod
  # active-host: "dev.getdbt.com" # dev
  active-project: "123456" # proj_1_prod
  # active-project: "234567" # proj_1_dev
"""

    @patch("builtins.open", new_callable=mock_open)
    def test_list_available_options(self, mock_file):
        self.mock_yaml_content = """version: "1"
context:
  active-host: "cloud.getdbt.com" # prod
  # active-host: "dev.getdbt.com" # dev
  active-project: "123456" # proj_1_prod
  # active-project: "234567" # proj_1_dev
  # active-project: "345678"
"""
        mock_file.return_value.read.return_value = self.mock_yaml_content
        
        # Redirect stdout to capture output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        list_available_options(Path("dummy/path/dbt_cloud.yml"))
        
        sys.stdout = sys.__stdout__  # Restore stdout
        
        output = captured_output.getvalue()
        self.assertIn("prod (active): cloud.getdbt.com", output)
        self.assertIn("dev (inactive): dev.getdbt.com", output)
        self.assertIn("proj_1_prod (active): 123456", output)
        self.assertIn("proj_1_dev (inactive): 234567", output)
        self.assertIn("345678 (inactive): 345678", output)

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_switch_active_project(self, mock_stdout, mock_file):
        mock_file.return_value.read.return_value = self.mock_yaml_content
        
        success = switch_active_property(Path("dummy/path/dbt_cloud.yml"), 'active-project', 'proj_1_dev')
        
        self.assertTrue(success)
        
        # Get all write calls
        write_calls = mock_file().write.call_args_list
        # Extract the string content from the first (and only) write call
        written_content = write_calls[0][0][0]

        self.assertIn('# active-project: "123456" # proj_1_prod', written_content)
        self.assertIn('active-project: "234567" # proj_1_dev', written_content)

    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_switch_active_host(self, mock_stdout, mock_file):
        mock_file.return_value.read.return_value = self.mock_yaml_content
        
        success = switch_active_property(Path("dummy/path/dbt_cloud.yml"), 'active-host', 'dev')
        
        self.assertTrue(success)
        
        written_content = mock_file().write.call_args[0][0]
        self.assertIn('# active-host: "cloud.getdbt.com" # prod', written_content)
        self.assertIn('active-host: "dev.getdbt.com" # dev', written_content)

    @patch("sys.argv", ["dbt-switch", "--list"])
    @patch("src.dbt_switch.main.list_available_options")
    @patch("sys.exit")
    def test_main_list(self, mock_exit, mock_list):
        main()
        mock_list.assert_called_once()
        mock_exit.assert_not_called()

    @patch("sys.argv", ["dbt-switch", "--proj", "proj_1_dev"])
    @patch("src.dbt_switch.main.switch_active_property")
    @patch("sys.exit")
    def test_main_switch_proj(self, mock_exit, mock_switch):
        main()
        mock_switch.assert_called_with(unittest.mock.ANY, 'active-project', 'proj_1_dev')
        mock_exit.assert_called_once_with(0)

    @patch("sys.argv", ["dbt-switch", "--host", "dev"])
    @patch("src.dbt_switch.main.switch_active_property")
    @patch("sys.exit")
    def test_main_switch_host(self, mock_exit, mock_switch):
        main()
        mock_switch.assert_called_with(unittest.mock.ANY, 'active-host', 'dev')
        mock_exit.assert_called_once_with(0)

if __name__ == "__main__":
    unittest.main()
