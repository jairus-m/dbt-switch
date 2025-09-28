"""
Argument parser using Click.
"""

import click

from dbt_switch.utils import logger, get_current_version
from dbt_switch.config.file_handler import init_config
from dbt_switch.config.input_handler import (
    add_user_config,
    delete_user_config,
    switch_user_config,
    list_projects,
    update_user_config_non_interactive,
    update_user_config_interactive,
)


@click.group(invoke_without_command=True)
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


@cli.command()
def init():
    """Initialize ~/.dbt/dbt_switch.yml"""
    init_config()


@cli.command()
@click.argument("project_name", required=False)
@click.option("--host", help="Project host URL (e.g., https://cloud.getdbt.com)")
@click.option("--project-id", type=int, help="dbt project ID")
def add(project_name, host, project_id):
    """Add a new project host and project_id"""
    add_user_config("add", project_name, host, project_id)


@cli.command("list")
def list_projects_cmd():
    """List all available projects"""
    list_projects()


@cli.command()
def delete():
    """Delete a project entry"""
    delete_user_config("delete")


@cli.command()
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
            logger.error("You must specify a project name when using --host or --project-id")
            click.echo("Usage: dbt-switch update PROJECT_NAME [--host HOST] [--project-id ID]")
        else:
            logger.error("Must specify a project name")
            click.echo("Usage: dbt-switch update PROJECT_NAME [OPTIONS]")
            click.echo("Use 'dbt-switch update --help' for more information.")
