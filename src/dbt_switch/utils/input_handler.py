from .config_handler import (
    add_config,
    update_project_host,
    update_project_id,
    delete_project_config,
)


def add_user_config_input(command: str):
    """
    Add a new project host and project_id to the dbt_switch.yml file.
    """
    if command == "add":
        project_name = input("Enter the project name: ")
        project_host = input("Enter the project host: ")
        project_id = int(input("Enter the project id: "))
        add_config(project_name, project_host, project_id)
    else:
        raise ValueError(f"Invalid command: {command}")


def update_user_config_input(arg: str):
    """
    Update a project host or project_id in the dbt_switch.yml file.
    """
    if arg == "host":
        project_name = input("Enter the project name: ")
        project_host = input("Enter the project host: ")
        update_project_host(project_name, project_host)
    elif arg == "project_id":
        project_name = input("Enter the project name: ")
        project_id = int(input("Enter the project id: "))
        update_project_id(project_name, project_id)
    else:
        raise ValueError(f"Invalid argument: {arg}")


def delete_user_config_input(command: str):
    """
    Delete a project entry from the dbt_switch.yml file.
    """
    if command == "delete":
        project_name = input("Enter the project name: ")
        delete_project_config(project_name)
    else:
        raise ValueError(f"Invalid command: {command}")
