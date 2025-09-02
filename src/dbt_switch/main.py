"""
Main entry point for dbt-switch.
"""

from dbt_switch.cli.parser import arg_parser


def main():
    arg_parser()


if __name__ == "__main__":
    main()
