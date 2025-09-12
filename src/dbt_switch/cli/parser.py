"""
Argument parser.
"""

import sys
import argparse

from dbt_switch.utils import logger, get_current_version
from dbt_switch.config.file_handler import init_config
from dbt_switch.config.input_handler import (
    add_user_config_input,
    update_user_config_input,
    delete_user_config_input,
    switch_user_config_input,
    list_projects,
)

__version__ = get_current_version()


def arg_parser():
    parser = argparse.ArgumentParser(description="dbt Cloud project and host switcher.")

    parser.add_argument("-p", "--project", help="Switch to the specified project")

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version number",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.add_parser("init", help="Initialize ~/.dbt/dbt_switch.yml")
    subparsers.add_parser("add", help="Add a new project host and project_id")
    subparsers.add_parser("list", help="List all available projects")
    subparsers.add_parser("delete", help="Delete a project entry")

    update_parser = subparsers.add_parser(
        "update", help="Update project host or project_id"
    )
    update_parser.add_argument(
        "--host", action="store_true", help="Update project host"
    )
    update_parser.add_argument(
        "--project-id", action="store_true", help="Update project ID"
    )

    args = parser.parse_args()

    if args.project:
        try:
            switch_user_config_input(args.project)
        except Exception as e:
            logger.error(f"Failed to switch to project '{args.project}': {e}")
            sys.exit(1)
        return

    if not args.command:
        parser.print_help()
        return

    if args.command == "init":
        init_config()

    if args.command == "list":
        list_projects()
        return

    if args.command == "add":
        add_user_config_input(args.command)

    if args.command == "delete":
        delete_user_config_input(args.command)

    if args.command == "update":
        if args.host:
            update_user_config_input("host")
        elif args.project_id:
            update_user_config_input("project_id")
        else:
            logger.warn("Please specify --host or --project-id")
