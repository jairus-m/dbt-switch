# dbt-switch

A simple CLI to switch between dbt Cloud projects and hosts.

## Usage

```bash
# Switch to a specific project and host
dbt-switch --proj proj_2 --host default

# Switch only the project (host stays the same)
dbt-switch --proj proj_1

# Switch only the host (project stays the same)
dbt-switch --host default

# See all available options
dbt-switch --list
```

## Example

Given a `dbt_cloud.yml` file like this:

```yaml
# dbt_cloud.yml
version: "1"
context:
  active-host: "cloud.getdbt.com" # default
  # active-host: "[identifier].us[#].dbt.com" # custom

  active-project: "123456" # proj_1
  # active-project: "234567" # proj_2
  # active-project: "345678" # proj_3
```

You can see the available options with `dbt-switch --list`:

```bash
$ dbt-switch --list

Available options in /Users/jairus.martinez/.dbt/dbt_cloud.yml:

active-hosts:
  - default (active): cloud.getdbt.com
  - custom (inactive): [identifier].us[#].dbt.com

active-projects:
  - proj_1 (active): 123456
  - proj_2 (inactive): 234567
  - proj_3 (inactive): 345678
```

The script identifies options by their comment (e.g., `# proj_1`). If a comment is not present, it will use the value of the property itself (e.g., the project ID or host URL).

Switch to the `custom` host and the `proj_3` project:

```bash
$ dbt-switch --host custom --proj proj_3

✓ Deactivated active-host: default
✓ Activated active-host: custom
Successfully updated dbt_cloud.yml
✓ Deactivated active-project: proj_1
✓ Activated active-project: proj_3
Successfully updated dbt_cloud.yml
```

The `dbt_cloud.yml` file will be updated to:

```yaml
# dbt_cloud.yml
version: "1"
context:
  # active-host: "cloud.getdbt.com" # default
  active-host: "[identifier].us[#].dbt.com" # custom

  # active-project: "123456" # proj_1
  # active-project: "234567" # proj_2
  active-project: "345678" # proj_3
```
