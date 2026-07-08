# Install the Odoo addon

This guide installs Odoo AI Agent System on Odoo 18 and prepares the first runtime connection.

## Quick path

1. Put this repository in your Odoo addons path.
2. Update the Odoo app list.
3. Install **AI Agent System**.
4. Give users the right access group.
5. Create a runtime and generate its API key.
6. Install the runtime daemon on the execution machine.
7. Create an agent and send a Project task to it.

## Requirements

| Requirement | Notes |
| --- | --- |
| Odoo | 18.0 |
| Odoo apps | `project`, `mail`, `base` |
| Python | Same version supported by your Odoo 18 deployment |
| Database | Any database supported by Odoo 18 |
| Runtime daemon | Required for real executions |

## Add the addon to Odoo

Clone or copy this repository into a directory included in `addons_path`.

Example Odoo config:

```ini
[options]
addons_path = /opt/odoo/odoo/addons,/opt/odoo/custom-addons
```

Then place the module as:

```text
/opt/odoo/custom-addons/odoo_agent
```

Restart Odoo and update the Apps list.

## Install from command line

```bash
odoo-bin -d <database> -i odoo_agent --stop-after-init
```

For test installation:

```bash
odoo-bin -d <database> -i odoo_agent --test-enable --stop-after-init
```

## Install from the UI

1. Open **Apps**.
2. Remove the Apps filter if needed.
3. Search for **AI Agent System**.
4. Click **Install**.

## Configure access

Assign users one of these groups:

| Group | Use it for |
| --- | --- |
| Agent User | Operators who assign tasks, send executions, and inspect logs/results. |
| Agent Admin | Administrators who manage runtimes, API keys, agents, skills, MCP servers, and mappings. |

## Create the first runtime

1. Go to **AI Agents → Runtimes**.
2. Create a runtime record.
3. Give it a clear name, for example `agent-worker-01`.
4. Generate an API key.
5. Copy the API key once and store it securely.

The runtime API key belongs to one runtime. Do not reuse it across machines.

## Install the runtime daemon

Use the runtime repository/package and follow [`runtime-installation.md`](runtime-installation.md).

At minimum the daemon needs:

- Odoo URL;
- runtime API key;
- runtime name;
- poll interval.

## Create the first agent

1. Go to **AI Agents → Agents**.
2. Create an agent.
3. Select the runtime.
4. Select an engine preset or **Custom CLI**.
5. Set `CLI Command`.
6. Add instructions, skills, MCP servers, limits, and retry policy.

Recommended first CLI command for a simple smoke test:

```text
python -c "print('runtime smoke ok')"
```

For real usage, configure the installed CLI:

```text
opencode run --instruction {instruction}
```

## Send a Project task

1. Open **Project**.
2. Create or open a task.
3. Assign the agent.
4. Click **Send to Agent**.
5. Open **Agent Executions** or **Agent Logs** from the task.

Expected result:

- execution starts as `queued`;
- runtime polls it;
- status becomes `running`;
- logs appear;
- result is posted back to the task;
- final status becomes `completed` or `failed`.

## Upgrade

Update the code and upgrade the module:

```bash
odoo-bin -d <database> -u odoo_agent --stop-after-init
```

After upgrading, restart the runtime daemon if the runtime contract changed.

## Uninstall

Uninstall from Apps or run:

```bash
odoo-bin -d <database> -u base --stop-after-init
```

Before uninstalling in production, export any execution logs/results you need for audit history.
