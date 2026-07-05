# Odoo AI Agent System

Replicates the Multica agent architecture natively within Odoo 18.0.

## Architecture

```
Odoo 18.0
├── odoo.agent.runtime  → External machines (N100, Mac Mini, etc.)
├── odoo.agent          → AI agents with instructions and skills
├── odoo.agent.skill    → Reusable instruction packs
├── odoo.agent.task     → Tasks assigned to AI agents
└── project.task        → Inherited: assign AI agents to Odoo tasks

External Runtime (Python daemon)
├── Polls Odoo API for pending tasks
├── Executes agent CLI (Hermes/OpenCode/OpenClaw)
└── Reports results back to Odoo
```

## Installation

1. Copy `odoo_agent/` to your Odoo addons directory
2. Update addons list and install the module
3. Go to AI Agents > Runtimes and register your external machines
4. Create agents and assign them to runtimes
5. Start the runtime daemon on each machine

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /api/agent/runtime/heartbeat | API Key | Runtime heartbeat |
| GET | /api/agent/runtime/poll | API Key | Poll for pending tasks |
| POST | /api/agent/task/{id}/start | API Key | Start a task |
| POST | /api/agent/task/{id}/complete | API Key | Complete a task |
| POST | /api/agent/runtime/register | Odoo User | Register a new runtime |

## Models

### odoo.agent.runtime
External machine running the daemon. Fields: name, machine_id, ip_address, status (offline/online/busy), last_seen, api_key, version, device_info.

### odoo.agent
AI agent entity. Fields: name, description, instructions, runtime_id, model, status (idle/working/error), avatar, skill_ids, max_concurrent_tasks, user_id.

### odoo.agent.skill
Reusable instruction pack. Fields: name, description, instructions, category (development/devops/analysis/communication/custom).

### odoo.agent.task
Task assigned to an AI agent. Fields: name, description, agent_id, project_id, task_id, status (pending/in_progress/completed/failed/cancelled), result, error_message.

## Runtime Daemon

```bash
cd odoo-agent-runtime
pip install -r requirements.txt

# Configure
export ODOO_URL=https://odoo.example.com
export API_KEY=your-runtime-api-key
export RUNTIME_NAME=n100-dev

# Run
python daemon.py
```

## Development

### Adding new agent CLIs

Edit `_run_agent_cli()` in `odoo-agent-runtime/daemon.py` to add new CLI mappings.

### Extending the API

Add new routes in `controllers/agent_api.py` following the existing pattern.

## License

LGPL-3
