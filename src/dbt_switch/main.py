import argparse
from dbt_switch.utils import init_config

def main():
    parser = argparse.ArgumentParser(description='dbt Cloud project and host switcher.')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    subparsers.add_parser('init', help='Initialize ~/.dbt/dbt_switch.yml')

    args = parser.parse_args()

    if args.command == 'init':
        init_config()

if __name__ == "__main__":
    main()