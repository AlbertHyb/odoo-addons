# Install the runtime daemon

The runtime daemon is the process that executes work outside Odoo. Install it on every machine that should run agent CLIs.

## Quick path

1. Create a runtime in Odoo.
2. Generate its API key.
3. Install the daemon on the target machine.
4. Enter Odoo URL and API key.
5. Start in manual mode first.
6. After a successful heartbeat, install it as a service if needed.

## Runtime package

The runtime is shipped separately from the Odoo addon so it can be installed on Linux, macOS, and Windows machines without copying an Odoo addons tree.

Expected files:

```text
daemon.py
install.sh
install.ps1
requirements.txt
.env.example
docs/
```

## Linux install

```bash
git clone https://github.com/nicolasramos-es/odoo-agent-runtime.git
cd odoo-agent-runtime
bash install.sh
```

Choose `manual` for the first run.

Manual start:

```bash
python3 daemon.py
```

Install as systemd service only after the manual run connects successfully.

## macOS install

```bash
git clone https://github.com/nicolasramos-es/odoo-agent-runtime.git
cd odoo-agent-runtime
bash install.sh
```

Choose:

- `manual` for first validation;
- `daemon` when you want launchd to keep it running.

## Windows install

```powershell
git clone https://github.com/nicolasramos-es/odoo-agent-runtime.git
cd odoo-agent-runtime
.\install.ps1
```

Choose:

- `manual` for first validation;
- `scheduled-task` when you want Windows Task Scheduler to keep it running.

## Installer prompts

The installers ask for:

| Prompt | Example | Notes |
| --- | --- | --- |
| Odoo URL | `https://odoo.example.com` | Must be reachable from the runtime host. |
| Runtime API key | `odoo_rt_...` | Generate it in Odoo. Required. |
| Runtime name | `agent-worker-01` | Human-readable machine name. |
| Poll interval | `10` | Seconds between polling loops. |
| Install mode | `manual`, `service`, `daemon`, `scheduled-task` | Depends on OS. |

If `.env` already exists, the installer must not overwrite it silently. It should ask and write `.env.new` when the operator declines overwrite.

## Manual `.env`

```env
ODOO_URL=https://odoo.example.com
API_KEY=your-runtime-api-key
RUNTIME_NAME=agent-worker-01
POLL_INTERVAL=10
```

Run:

```bash
python3 -m pip install -r requirements.txt
python3 daemon.py
```

## Validate connectivity

In Odoo:

1. Open **AI Agents → Runtimes**.
2. Confirm `Last Seen` updates.
3. Confirm status is `Online` or `Busy`.
4. Send a smoke-test task.
5. Confirm logs appear in the execution.

## Install CLIs

The runtime only orchestrates commands. It does not install every agent CLI for you.

Install the tools required by the agents assigned to that runtime:

- Codex-compatible CLI;
- Hermes CLI/gateway;
- OpenCode CLI;
- OpenClaw CLI;
- Claude Code CLI;
- any custom internal CLI.

Then configure each Odoo agent's `CLI Command` accordingly.

## Safe first production rollout

1. Create a dedicated runtime user on the machine.
2. Install only required CLIs.
3. Use one runtime API key per machine.
4. Start with one low-risk Project task.
5. Validate logs, result, retry, failure, and cancellation.
6. Only then enable daemon/service mode.
