"""
Argument parser using Click.
"""

import click

from dbt_switch.utils import logger, get_current_version
from dbt_switch.config.file_handler import init_config
from dbt_switch.agent import SKILL_PROMPT_INIT, SKILL_PROMPT_USAGE
from dbt_switch.config.input_handler import (
    add_user_config,
    delete_user_config,
    switch_user_config,
    list_projects,
    update_user_config_non_interactive,
    update_user_config_interactive,
)


CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option("-p", "--project", help="Switch to the specified project")
@click.version_option(version=get_current_version(), prog_name="dbt-switch")
@click.pass_context
def cli(ctx, project):
    """dbt Cloud project and host switcher."""
    if project:
        try:
            switch_user_config(project)
        except Exception as e:
            logger.error(f"Failed to switch to project '{project}': {e}")
            ctx.exit(1)
        return

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option("--init", "mode", flag_value="init", help="Prompt for first-time setup: merging dbt_cloud.yml files and configuring dbt-switch")
@click.option("--usage", "mode", flag_value="usage", help="Prompt for day-to-day usage: switching, adding, updating, and deleting projects")
def skill(mode):
    """Print an agent skill prompt for AI-assisted setup (--init) or usage (--usage).

    Run without flags to print both prompts.
    """
    if mode == "init":
        click.echo(SKILL_PROMPT_INIT)
    elif mode == "usage":
        click.echo(SKILL_PROMPT_USAGE)
    else:
        click.echo(SKILL_PROMPT_INIT)
        click.echo("\n---\n")
        click.echo(SKILL_PROMPT_USAGE)


@cli.command(context_settings=CONTEXT_SETTINGS)
def init():
    """Initialize ~/.dbt/dbt_switch.yml"""
    init_config()


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("project_name", required=False)
@click.option("--host", help="Project host URL (e.g., https://cloud.getdbt.com)")
@click.option("--project-id", type=int, help="dbt project ID")
def add(project_name, host, project_id):
    """Add a new project host and project_id"""
    add_user_config("add", project_name, host, project_id)


@cli.command("list", context_settings=CONTEXT_SETTINGS)
def list_projects_cmd():
    """List all available projects"""
    list_projects()


@cli.command(context_settings=CONTEXT_SETTINGS)
def delete():
    """Delete a project entry"""
    delete_user_config("delete")


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("project_name", required=False)
@click.option("--host", help="Update project host URL (e.g., https://cloud.getdbt.com)")
@click.option("--project-id", type=int, help="Update dbt project ID")
def update(project_name, host, project_id):
    """Update project host or project_id"""
    if project_name:
        if host or project_id:
            # Non-interactive mode: update specified parameters
            update_user_config_non_interactive(project_name, host, project_id)
        else:
            # Interactive mode: show menu for updates
            update_user_config_interactive(project_name)
    else:
        if host or project_id:
            logger.error(
                "You must specify a project name when using --host or --project-id"
            )
            click.echo(
                "Usage: dbt-switch update PROJECT_NAME [--host HOST] [--project-id ID]"
            )
        else:
            logger.error("Must specify a project name")
            click.echo("Usage: dbt-switch update PROJECT_NAME [OPTIONS]")
            click.echo("Use 'dbt-switch update --help' for more information.")
