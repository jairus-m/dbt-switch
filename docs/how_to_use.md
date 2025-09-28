# How to Use dbt-switch

## Overview

`dbt-switch` helps you:
1. **Manage project configurations** in `~/.dbt/dbt_switch.yml`
2. **Switch active projects** in your `~/.dbt/dbt_cloud.yml` file

## Prerequisites: Merging dbt_cloud.yml Files

**Important:** Before using `dbt-switch`, you must manually merge your `dbt_cloud.yml` files from different dbt Cloud accounts into a single file.

### Why This Is Needed

When you work with multiple dbt Cloud accounts, each account provides its own `dbt_cloud.yml` file with account-specific projects and tokens. The dbt Cloud CLI can only read from one `~/.dbt/dbt_cloud.yml` file, so you need to combine all projects into this single file.

### How to Merge

1. **Download** each `dbt_cloud.yml` file from your different dbt Cloud accounts ([instructions here](https://docs.getdbt.com/docs/cloud/configure-cloud-cli#configure-the-dbt-cli))
2. **Copy** all `projects` entries from each file
3. **Paste** them into a single `~/.dbt/dbt_cloud.yml` file
4. **Keep** one `version` and one `context` section

### Example: Before and After

**Before (separate files):**
```yaml
# Account A's dbt_cloud.yml
projects:
  - project-name: "Alpha Analytics"
    project-id: "12345"
    account-host: "cloud.getdbt.com"
    token-value: "dbtu_alpha_token"

# Account B's dbt_cloud.yml
projects:
  - project-name: "Beta Corp"
    project-id: "67890"
    account-host: "cloud.getdbt.com"
    token-value: "dbtu_beta_token"
```

**After (merged into one file):**
```yaml
# Single ~/.dbt/dbt_cloud.yml
version: "1"
context:
  active-host: "cloud.getdbt.com"
  active-project: "12345"
projects:
  - project-name: "Alpha Analytics"
    project-id: "12345"
    account-host: "cloud.getdbt.com"
    token-value: "dbtu_alpha_token"
  - project-name: "Beta Corp"
    project-id: "67890"
    account-host: "cloud.getdbt.com"
    token-value: "dbtu_beta_token"
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

Your merged dbt Cloud configuration file should look something like this (after following the merge steps above):

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

```bash
# Initialize configuration file
dbt-switch init

# Add a new project (interactive mode)
dbt-switch add
# Enter project name: my-project
# Enter project host: cloud.getdbt.com
# Enter project id: 123456

# Add a new project (non-interactive mode - great for automation!)
dbt-switch add my-project --host cloud.getdbt.com --project-id 123456

# Update project (interactive mode)
dbt-switch update my-project

# Update project host (non-interactive)
dbt-switch update my-project --host staging.getdbt.com

# Update project ID (non-interactive)
dbt-switch update my-project --project-id 99999

# Update both host and project ID at once
dbt-switch update my-project --host staging.getdbt.com --project-id 99999

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

## Examples

### 1. Initialize and add projects:

```bash
$ dbt-switch init
Initialized /Users/username/.dbt/dbt_switch.yml

$ dbt-switch add
Enter the project name: alpha-analytics
Enter the project host: cloud.getdbt.com
Enter the project id: 12345
Added project 'alpha-analytics' with host 'cloud.getdbt.com' and project_id 12345

$ dbt-switch add beta-corp --host cloud.getdbt.com --project-id 67890
Added project 'beta-corp' with host 'cloud.getdbt.com' and project_id 67890
```

### 2. Switch between projects:

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

### 3. Update project configurations:

```bash
# Interactive mode - shows current config and menu
$ dbt-switch update prod-analytics
Current configuration for 'prod-analytics':
  Host: cloud.getdbt.com
  Project ID: 12345

What would you like to update?
1. Host only
2. Project ID only
3. Both host and project ID
Enter your choice (1-3): 1

Enter the new project host: staging.getdbt.com
Updated project 'prod-analytics' with host 'staging.getdbt.com'

# Non-interactive mode - direct updates
$ dbt-switch update prod-analytics --host staging.getdbt.com --project-id 99999
Updated project 'prod-analytics' with host 'staging.getdbt.com' and project_id 99999
```

## Command Reference

| Command | Description |
|---------|-------------|
| `dbt-switch init` | Initialize the `~/.dbt/dbt_switch.yml` file |
| `dbt-switch add` | Add a new project configuration (interactive mode) |
| `dbt-switch add PROJECT --host HOST --project-id ID` | Add a new project configuration (non-interactive mode) |
| `dbt-switch list` | List all configured projects with their details |
| `dbt-switch update PROJECT` | Update a project configuration (interactive mode) |
| `dbt-switch update PROJECT --host HOST` | Update a project's host (non-interactive mode) |
| `dbt-switch update PROJECT --project-id ID` | Update a project's ID (non-interactive mode) |
| `dbt-switch update PROJECT --host HOST --project-id ID` | Update both host and project ID (non-interactive mode) |
| `dbt-switch delete` | Delete a project configuration |
| `dbt-switch -p PROJECT` | Switch to the specified project |
| `dbt-switch --project PROJECT` | Switch to the specified project (long form) |
| `dbt-switch --help` | Show help message |

## How It Works

1. **Store configurations**: `dbt-switch` maintains your project configurations in `~/.dbt/dbt_switch.yml`
2. **Update dbt Cloud config**: When you switch projects, it updates the `active-host` and `active-project` fields in your `~/.dbt/dbt_cloud.yml`
3. **Preserve your data**: All other fields in `dbt_cloud.yml` (like tokens and project lists) are preserved

## Interactive vs Non-Interactive Modes

### Interactive Mode
- **When to use**: Quick setup, exploring options, or when you're unsure of exact values
- **Benefits**: Guided prompts, current configuration display, menu-driven selection
- **Examples**:
  ```bash
  dbt-switch add                    # Prompts for all details
  dbt-switch update my-project      # Shows menu for what to update
  ```

### Non-Interactive Mode
- **When to use**: Automation, scripts, CI/CD pipelines, or when you know exact values
- **Benefits**: Fast execution, scriptable, no user interaction required
- **Examples**:
  ```bash
  dbt-switch add my-project --host cloud.getdbt.com --project-id 123456
  dbt-switch update my-project --host staging.getdbt.com --project-id 99999
  ```

### Combined Updates
- **When to use**: When you need to update both host and project ID at the same time
- **Benefits**: Single command to update all project details, efficient for migrations
- **Examples**:
  ```bash
  dbt-switch update my-project --host new-host.getdbt.com --project-id 99999
  ```