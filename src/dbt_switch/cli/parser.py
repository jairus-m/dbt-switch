"""
Argument parser.
"""

import argparse

from dbt_switch.utils.logger import logger
from dbt_switch.config.file_handler import init_config
from dbt_switch.config.input_handler import (
    add_user_config_input,
    update_user_config_input,
    delete_user_config_input,
)


def arg_parser():
    parser = argparse.ArgumentParser(description="dbt Cloud project and host switcher.")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.add_parser("init", help="Initialize ~/.dbt/dbt_switch.yml")
    subparsers.add_parser("add", help="Add a new project host and project_id")
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

    if args.command == "init":
        init_config()

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
