# User guide

This guide explains the daily workflow for Project users and agent operators.

## Quick path

1. Open a Project task.
2. Assign an agent.
3. Click **Send to Agent**.
4. Watch the status badge.
5. Use **Agent Communications** to talk with the agent inside the task.
6. Open logs when needed.
7. Retry, cancel, or review the final result.

## Assign an agent

Use the **AI Agent** field on a Project task. The selected agent determines:

- which runtime will execute the work;
- which CLI command will run;
- which instructions, skills, and MCP servers are available;
- timeout, retry, and concurrency limits.

## Send a task to an agent

Click **Send to Agent**.

Odoo creates an **Agent Execution** linked to the task. A task can have multiple executions over time, which keeps retries and follow-up attempts auditable.

## Understand statuses

| Status | Meaning |
| --- | --- |
| `queued` | Odoo created the execution and is waiting for the runtime to poll it. |
| `running` | Runtime started the execution. |
| `waiting_input` | Execution needs external input or is paused by the runtime. |
| `completed` | Runtime returned a final result. |
| `failed` | Runtime or CLI failed and reported an error. |
| `cancelled` | Cancellation was acknowledged. |

## Read logs

Open **Agent Logs** from the task or execution.

Logs are useful for:

- verifying which command ran;
- seeing progress;
- debugging CLI failures;
- proving what happened during execution.

## Retry

Use **Retry** when a failed execution can be safely attempted again.

A retry creates a new execution attempt instead of overwriting the old result.

## Cancel

Use **Cancel** when the runtime should stop working on the execution.

Cancellation is cooperative: Odoo requests cancellation, and the runtime must acknowledge it.

## Use `@mentions`

Mention another agent in the prompt/task content:

```text
Prepare onboarding E2E cases and ask @qa to review edge cases.
```

Odoo creates a child execution for the mentioned agent. The parent and child executions remain linked for traceability.

## Good task prompts

Good:

```text
Prepare E2E test cases for tenant onboarding.
Include happy path, failed invitation, expired token, and permission edge cases.
Post a concise final checklist.
```

Weak:

```text
Do QA.
```

Agents are more useful when tasks include objective, scope, constraints, and expected output.


## Chat with agents

The primary chat experience lives inside the Project task, in the **Agent Communications** tab.

Use it for follow-up instructions, questions, reviews, and agent-to-user progress messages without leaving the task context.

Agent communications use the same execution system as Project tasks. When you send a message to an agent, Odoo creates a queued chat execution so the runtime can process it with full traceability.

Flow:

1. User opens a Project task.
2. User writes a message in **Agent Communications**.
3. Odoo creates a chat message linked to the task.
4. Odoo creates a queued chat execution.
5. Runtime polls the execution.
6. Runtime streams logs and may send intermediate messages.
7. Runtime completes the execution.
8. Odoo creates the final agent reply from the result.

The regular Odoo chatter remains useful for audit events and followers. The **Agent Communications** tab is the operational conversation with agents.

Use **AI Agents → Chats** to inspect all messages globally, including delivery state, linked execution, and related Project task.

API flow:

1. External UI sends a chat message to an agent.
2. Odoo creates a chat message and a queued execution.
3. Runtime polls the execution.
4. Runtime streams logs and may send intermediate messages.
5. Runtime completes the execution.
6. Odoo creates the final agent reply from the result.
