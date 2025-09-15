"""
Argument parser using Click.
"""

import click

from dbt_switch.utils import logger, get_current_version
from dbt_switch.config.file_handler import init_config
from dbt_switch.config.input_handler import (
    add_user_config_input,
    update_user_config_input,
    delete_user_config_input,
    switch_user_config_input,
    list_projects,
)


@click.group(invoke_without_command=True)
@click.option("-p", "--project", help="Switch to the specified project")
@click.version_option(version=get_current_version(), prog_name="dbt-switch")
@click.pass_context
def cli(ctx, project):
    """dbt Cloud project and host switcher."""
    if project:
        try:
            switch_user_config_input(project)
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
def add():
    """Add a new project host and project_id"""
    add_user_config_input("add")


@cli.command("list")
def list_projects_cmd():
    """List all available projects"""
    list_projects()


@cli.command()
def delete():
    """Delete a project entry"""
    delete_user_config_input("delete")


@cli.command()
@click.option("--host", is_flag=True, help="Update project host")
@click.option("--project-id", is_flag=True, help="Update project ID")
def update(host, project_id):
    """Update project host or project_id"""
    if host and project_id:
        logger.error(
            "Cannot update both host and project-id at the same time. Choose one."
        )
        return
    elif host:
        update_user_config_input("host")
    elif project_id:
        update_user_config_input("project_id")
    else:
        logger.error("Must specify either --host or --project-id")
        click.echo("Use 'dbt-switch update --help' for more information.")
