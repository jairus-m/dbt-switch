# dbt-switch

This is a simple CLI tool to manage and switch between dbt Cloud projects and hosts. This util was inspired by working in professional services/consulting and running into minor pain points with managing multuple dbt Cloud projects that exist in different accounts. The crux of the issue is documented in this dbt forum post: [dbt Cloud CLI - Connect to Mulitple Hosts](https://discourse.getdbt.com/t/dbt-cloud-cli-connect-to-multiple-hosts/14075).

For the `dbt_cloud.yml` configuration file to work properly with mulitple accounts, the `context` key needs to be updated with an active project's host and project_id:

```yml
context:
  active-host: "cloud.getdbt.com"
  active-project: "12345"
```

As seen in the [dbt Cloud CLI docs](https://docs.getdbt.com/docs/cloud/configure-cloud-cli#configure-the-dbt-cli), you need to set the correct active host and project ID before using the dbt Cloud CLI with your desired project.  Espeacially if you have a custom `active-host` URL, you have manually swap out the `active-host` in your `dbt_cloud.yml` (in addition to swapping the `active-project`)every time you switch to a new dbt Cloud account's project.

Instead of manually swapping out `active-host` and `active-project` in `dbt_cloud.yml`, this utility allows you to define projects and their associated host/project ID and easily switch between them from the CLI.

## Requirements
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Proper [dbt Cloud CLI credentials/config](https://docs.getdbt.com/docs/cloud/configure-cloud-cli#configure-the-dbt-cli) that exist in your `~/.dbt/dbt_cloud.yml` file 

## Installation

```bash
uv tool install dbt-switch
```

## Overview

`dbt-switch` helps you:
1. **Manage project configurations** in `~/.dbt/dbt_switch.yml`
2. **Switch active projects** in your `~/.dbt/dbt_cloud.yml` file

## Quick Start

```bash
# Initialize the configuration file
dbt-switch init

# Add a new project configuration
dbt-switch add

# List all configured projects
dbt-switch list

# Switch to a project
dbt-switch --project alpha-analytics
dbt-switch -p beta-corp
```

## Configuration Files

### 1. dbt_switch.yml (`~/.dbt/dbt_switch.yml`)

This file stores your project configurations:

```yaml
profiles:
  alpha-analytics:
    host: cloud.getdbt.com
    project_id: 12345
  beta-corp:
    host: cloud.getdbt.com  
    project_id: 67890
  gamma-solutions:
    host: xyz123.us1.dbt.com
    project_id: 54321
```

### 2. dbt_cloud.yml (`~/.dbt/dbt_cloud.yml`)

Your standard dbt Cloud configuration file should look something like:

>Note: You will have to manually merge the `projects` from your different dbt Cloud accounts into a single `~/.dbt/dbt_cloud.yml` file.

```yaml
version: "1"
context:
  active-host: "cloud.getdbt.com"
  active-project: "12345"
projects:
  - project-name: "Client Alpha Analytics"
    project-id: "12345"
    account-name: "Alpha Industries"
    account-id: "11111"
    account-host: "cloud.getdbt.com"
    token-name: "cloud-cli-alpha"
    token-value: "dbtu_alpha_token_here"

  - project-name: "Beta Corp Reporting" # Originally from its own dbt_cloud.yml, manually "merged" (paseted) in
    project-id: "67890"
    account-name: "Beta Corporation"
    account-id: "22222"
    account-host: "cloud.getdbt.com"
    token-name: "cloud-cli-beta"
    token-value: "dbtu_beta_token_here"

  - project-name: "Gamma Solutions Data" # Originally from its own dbt_cloud.yml, manually "merged" (paseted) in
    project-id: "54321"
    account-name: "Gamma Solutions (Partner)"
    account-id: "33333"
    account-host: "xyz123.us1.dbt.com"
    token-name: "cloud-cli-gamma"
    token-value: "dbtu_gamma_token_here"
```

## Usage

### Project Management

>Note: These commands are interactive and trigger a bash prompt!

```bash
# Initialize configuration file
dbt-switch init

# Add a new project
dbt-switch add
# Enter project name: my-project
# Enter project host: cloud.getdbt.com
# Enter project id: 123456

# Update project host
dbt-switch update --host

# Update project ID  
dbt-switch update --project-id

# Delete a project
dbt-switch delete

# List all projects
dbt-switch list
```

### Project Switching

```bash
# Switch to a project (long form)
dbt-switch --project alpha-analytics

# Switch to a project (short form)
dbt-switch -p beta-corp

# Get help
dbt-switch --help
```

## Example

1. **Initialize and add projects:**

  ```bash
  $ dbt-switch init
  Initialized /Users/username/.dbt/dbt_switch.yml

  $ dbt-switch add
  Enter the project name: alpha-analytics
  Enter the project host: cloud.getdbt.com
  Enter the project id: 12345
  Added project 'alpha-analytics' with host 'cloud.getdbt.com' and project_id 12345

  $ dbt-switch add
  Enter the project name: beta-corp  
  Enter the project host: cloud.getdbt.com
  Enter the project id: 67890
  Added project 'beta-corp' with host 'cloud.getdbt.com' and project_id 67890
  ```

2. **Switch between projects:**

  ```bash
  $ dbt-switch -p alpha-analytics
  Successfully switched to project 'alpha-analytics'
  ✓ Set active host: cloud.getdbt.com
  ✓ Set active project: 12345

  $ dbt-switch -p beta-corp  
  Successfully switched to project 'beta-corp'
  ✓ Set active host: cloud.getdbt.com
  ✓ Set active project: 67890
  
  $ dbt-switch list
  Available projects:
    alpha-analytics (cloud.getdbt.com, ID: 12345)
  * beta-corp      (cloud.getdbt.com, ID: 67890) [ACTIVE]
  ```

## Commands

| Command | Description |
|---------|-------------|
| `dbt-switch init` | Initialize the `~/.dbt/dbt_switch.yml` file |
| `dbt-switch add` | Add a new project configuration |
| `dbt-switch list` | List all configured projects with their details |
| `dbt-switch update --host` | Update a project's host |
| `dbt-switch update --project-id` | Update a project's ID |
| `dbt-switch delete` | Delete a project configuration |
| `dbt-switch -p PROJECT` | Switch to the specified project |
| `dbt-switch --project PROJECT` | Switch to the specified project (long form) |
| `dbt-switch --help` | Show help message |

## How It Works

1. **Store configurations**: `dbt-switch` maintains your project configurations in `~/.dbt/dbt_switch.yml`
2. **Update dbt Cloud config**: When you switch projects, it updates the `active-host` and `active-project` fields in your `~/.dbt/dbt_cloud.yml`
3. **Preserve your data**: All other fields in `dbt_cloud.yml` (like tokens and project lists) are preserved