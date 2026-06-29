"""
Unit tests for agent skill prompts.
"""

from dbt_switch.prompts.skills import SKILL_PROMPT_INIT, SKILL_PROMPT_USAGE


class TestSkillPromptInit:
    def test_is_non_empty_string(self):
        assert isinstance(SKILL_PROMPT_INIT, str)
        assert len(SKILL_PROMPT_INIT) > 0

    def test_no_leading_or_trailing_whitespace(self):
        assert SKILL_PROMPT_INIT == SKILL_PROMPT_INIT.strip()

    def test_contains_setup_commands(self):
        assert "dbt-switch init" in SKILL_PROMPT_INIT
        assert "dbt-switch add" in SKILL_PROMPT_INIT
        assert "dbt-switch list" in SKILL_PROMPT_INIT
        assert "dbt-switch -p" in SKILL_PROMPT_INIT

    def test_describes_yaml_structure(self):
        assert "version" in SKILL_PROMPT_INIT
        assert "projects" in SKILL_PROMPT_INIT
        assert "account-host" in SKILL_PROMPT_INIT
        assert "project-id" in SKILL_PROMPT_INIT

    def test_references_dbt_cloud_yml(self):
        assert "dbt_cloud.yml" in SKILL_PROMPT_INIT

    def test_add_command_field_mapping(self):
        assert "--host" in SKILL_PROMPT_INIT
        assert "--project-id" in SKILL_PROMPT_INIT


class TestSkillPromptUsage:
    def test_is_non_empty_string(self):
        assert isinstance(SKILL_PROMPT_USAGE, str)
        assert len(SKILL_PROMPT_USAGE) > 0

    def test_no_leading_or_trailing_whitespace(self):
        assert SKILL_PROMPT_USAGE == SKILL_PROMPT_USAGE.strip()

    def test_contains_switch_commands(self):
        assert "dbt-switch -p" in SKILL_PROMPT_USAGE
        assert "dbt-switch --project" in SKILL_PROMPT_USAGE
        assert "dbt-switch list" in SKILL_PROMPT_USAGE

    def test_contains_crud_commands(self):
        assert "dbt-switch add" in SKILL_PROMPT_USAGE
        assert "dbt-switch update" in SKILL_PROMPT_USAGE
        assert "dbt-switch delete" in SKILL_PROMPT_USAGE

    def test_references_skill_init_for_new_users(self):
        assert "dbt-switch skill --init" in SKILL_PROMPT_USAGE
