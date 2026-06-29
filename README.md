# dbt-switch

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/jairus-m/dbt-switch)

A simple CLI tool to manage and switch between dbt Cloud projects and hosts. Solves the pain point of manually updating `active-host` and `active-project` in your `dbt_cloud.yml` when working with multiple dbt Cloud accounts. Read more about it [here](https://www.brooklyndata.co/ideas/2025/10/16/managing-multiple-dbt-cloud-projects-try-dbt-switch)!

The crux of the issue is documented in this dbt forum post: [dbt Cloud CLI - Connect to Mulitple Hosts](https://discourse.getdbt.com/t/dbt-cloud-cli-connect-to-multiple-hosts/14075).

> **Two ways to use dbt-switch:** run the CLI commands yourself, or let an AI agent handle setup and day-to-day usage for you. Both paths are documented below.




## Requirements
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [dbt Cloud CLI config](https://docs.getdbt.com/docs/cloud/configure-cloud-cli#configure-the-dbt-cli) in your `~/.dbt/dbt_cloud.yml` file

## Important Setup Step

**You must manually merge your dbt_cloud.yml files from different accounts into one file.**

If you work with multiple dbt Cloud accounts, you'll have separate `dbt_cloud.yml` files for each account. You need to combine all the `projects` sections into a single `~/.dbt/dbt_cloud.yml` file before using `dbt-switch`.

## Documentation
📚 See the [Complete Usage Guide](docs/how_to_use.md#configuration-files) for detailed examples of the merged file structure.

## Installation

```bash
uv tool install dbt-switch
```

## Quick Start

```bash
# Initialize the configuration file
dbt-switch init

# Add a new project (interactive)
dbt-switch add

# Add a new project (non-interactive)
dbt-switch add my-project --host https://cloud.getdbt.com --project-id 12345

# List all configured projects
dbt-switch list

# Switch to a project
dbt-switch -p my-project
```

## AI-Assisted Setup & Usage

dbt-switch ships with agent skill prompts that you can pass directly to an AI (e.g. Claude Code) to automate setup or day-to-day project management.

```bash
# Print the setup prompt (merging dbt_cloud.yml files + configuring dbt-switch)
dbt-switch skill --init

# Print the usage prompt (switching, adding, updating, deleting projects)
dbt-switch skill --usage

# Print both
dbt-switch skill
```

**How to use:** run one of the commands above from within an AI coding session (e.g. Claude Code) or copy the output and paste it into your AI assistant as a system/user prompt. The agent will guide you through the workflow — you just download the files (for `--init`) or describe what you want to do (for `--usage`).

## Key Features

- Manage multiple dbt Cloud projects across different accounts
- Switch projects instantly with a simple command
- Interactive and non-interactive modes for different workflows
- Update project configurations easily (host, project ID, or both)

## Documentation

**[Complete Usage Guide](docs/how_to_use.md)** - Detailed documentation with examples, configuration files, and command reference

## How It Works

1. **Store configurations**: Define your projects in `~/.dbt/dbt_switch.yml`
2. **Switch instantly**: Update `active-host` and `active-project` in your `~/.dbt/dbt_cloud.yml`
3. **Keep your data**: All tokens and project configurations are preserved

**Example workflow:**
```bash
# Add your projects
dbt-switch add alpha --host cloud.getdbt.com --project-id 12345
dbt-switch add beta --host xyz123.us1.dbt.com --project-id 67890

# Switch between them
dbt-switch -p alpha    # Now using Alpha Industries project
dbt-switch -p beta     # Now using Beta Corp project
```
