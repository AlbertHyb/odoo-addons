# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
from datetime import datetime

from odoo import http
from odoo.http import request, Response


class AgentApiController(http.Controller):

    def _authenticate_runtime(self):
        """Authenticate a runtime by API key."""
        api_key = request.params.get('api_key') or request.httprequest.headers.get('X-API-Key')
        if not api_key:
            return None
        runtime = request.env['odoo.agent.runtime'].sudo().search([
            ('api_key', '=', api_key),
        ], limit=1)
        return runtime

    def _json_response(self, data, status=200):
        return Response(
            json.dumps(data, default=str),
            status=status,
            content_type='application/json',
        )

    @http.route(
        '/api/agent/runtime/heartbeat',
        type='http',
        methods=['POST'],
        auth='none',
        csrf=False,
    )
    def heartbeat(self, **kwargs):
        """Runtime sends heartbeat to confirm it's alive."""
        runtime = self._authenticate_runtime()
        if not runtime:
            return self._json_response({'error': 'Invalid API key'}, 401)
        runtime.sudo().write({
            'status': 'online',
            'last_seen': datetime.now(),
            'version': kwargs.get('version', runtime.version),
            'device_info': kwargs.get('device_info', runtime.device_info),
        })
        return self._json_response({
            'status': 'ok',
            'runtime_id': runtime.id,
            'runtime_name': runtime.name,
        })

    @http.route(
        '/api/agent/runtime/poll',
        type='http',
        methods=['GET'],
        auth='none',
        csrf=False,
    )
    def poll_tasks(self, **kwargs):
        """Runtime polls for pending tasks assigned to its agents."""
        runtime = self._authenticate_runtime()
        if not runtime:
            return self._json_response({'error': 'Invalid API key'}, 401)

        runtime.sudo().write({'last_seen': datetime.now()})

        agent_ids = runtime.agent_ids.ids
        if not agent_ids:
            return self._json_response({'tasks': []})

        limit = int(kwargs.get('limit', 10))
        tasks = request.env['odoo.agent.task'].sudo().search([
            ('status', '=', 'pending'),
            ('agent_id', 'in', agent_ids),
        ], limit=limit)

        task_data = []
        for task in tasks:
            task_data.append({
                'id': task.id,
                'name': task.name,
                'description': task.description,
                'agent_id': task.agent_id.id,
                'agent_name': task.agent_id.name,
                'project_id': task.project_id.id if task.project_id else None,
                'task_id': task.task_id.id if task.task_id else None,
                'created_at': str(task.create_date),
            })

        return self._json_response({'tasks': task_data})

    @http.route(
        '/api/agent/task/<int:task_id>/start',
        type='http',
        methods=['POST'],
        auth='none',
        csrf=False,
    )
    def start_task(self, task_id, **kwargs):
        """Runtime marks a task as in_progress."""
        runtime = self._authenticate_runtime()
        if not runtime:
            return self._json_response({'error': 'Invalid API key'}, 401)

        task = request.env['odoo.agent.task'].sudo().browse(task_id)
        if not task.exists():
            return self._json_response({'error': 'Task not found'}, 404)

        if task.agent_id.runtime_id != runtime:
            return self._json_response({'error': 'Task not assigned to this runtime'}, 403)

        task.action_start()
        return self._json_response({
            'status': 'ok',
            'task_id': task.id,
            'new_status': 'in_progress',
        })

    @http.route(
        '/api/agent/task/<int:task_id>/complete',
        type='http',
        methods=['POST'],
        auth='none',
        csrf=False,
    )
    def complete_task(self, task_id, **kwargs):
        """Runtime reports task completion."""
        runtime = self._authenticate_runtime()
        if not runtime:
            return self._json_response({'error': 'Invalid API key'}, 401)

        task = request.env['odoo.agent.task'].sudo().browse(task_id)
        if not task.exists():
            return self._json_response({'error': 'Task not found'}, 404)

        if task.agent_id.runtime_id != runtime:
            return self._json_response({'error': 'Task not assigned to this runtime'}, 403)

        status = kwargs.get('status', 'completed')
        result = kwargs.get('result')
        error_message = kwargs.get('error_message')

        if status == 'failed':
            task.action_fail(error_message=error_message)
        else:
            task.action_complete(result=result)

        return self._json_response({
            'status': 'ok',
            'task_id': task.id,
            'new_status': status,
        })

    @http.route(
        '/api/agent/task/<int:task_id>/log',
        type='http',
        methods=['POST'],
        auth='none',
        csrf=False,
    )
    def add_task_log(self, task_id, **kwargs):
        """Runtime sends a log entry for a task (streaming)."""
        runtime = self._authenticate_runtime()
        if not runtime:
            return self._json_response({'error': 'Invalid API key'}, 401)

        task = request.env['odoo.agent.task'].sudo().browse(task_id)
        if not task.exists():
            return self._json_response({'error': 'Task not found'}, 404)

        if task.agent_id.runtime_id != runtime:
            return self._json_response({'error': 'Task not assigned to this runtime'}, 403)

        level = kwargs.get('level', 'info')
        message = kwargs.get('message', '')
        command = kwargs.get('command')
        exit_code = kwargs.get('exit_code')

        log = request.env['odoo.agent.log'].sudo().create({
            'agent_task_id': task_id,
            'level': level,
            'message': message,
            'command': command,
            'exit_code': exit_code and int(exit_code),
            'timestamp': datetime.now(),
        })

        return self._json_response({
            'status': 'ok',
            'log_id': log.id,
        })

    @http.route(
        '/api/agent/task/<int:task_id>/logs',
        type='http',
        methods=['GET'],
        auth='none',
        csrf=False,
    )
    def get_task_logs(self, task_id, **kwargs):
        """Get all logs for a task."""
        runtime = self._authenticate_runtime()
        if not runtime:
            return self._json_response({'error': 'Invalid API key'}, 401)

        task = request.env['odoo.agent.task'].sudo().browse(task_id)
        if not task.exists():
            return self._json_response({'error': 'Task not found'}, 404)

        level = kwargs.get('level')
        limit = int(kwargs.get('limit', 100))

        domain = [('agent_task_id', '=', task_id)]
        if level:
            domain.append(('level', '=', level))

        logs = request.env['odoo.agent.log'].sudo().search(domain, limit=limit)

        log_data = []
        for log in logs:
            log_data.append({
                'id': log.id,
                'timestamp': str(log.timestamp),
                'level': log.level,
                'message': log.message,
                'command': log.command,
                'exit_code': log.exit_code,
            })

        return self._json_response({'logs': log_data})

    @http.route(
        '/api/agent/runtime/register',
        type='http',
        methods=['POST'],
        auth='user',
        csrf=False,
    )
    def register_runtime(self, **kwargs):
        """Register a new runtime (requires Odoo auth)."""
        name = kwargs.get('name')
        machine_id = kwargs.get('machine_id')
        if not name or not machine_id:
            return self._json_response({'error': 'name and machine_id required'}, 400)

        runtime = request.env['odoo.agent.runtime'].sudo().create({
            'name': name,
            'machine_id': machine_id,
            'ip_address': kwargs.get('ip_address'),
            'version': kwargs.get('version'),
            'device_info': kwargs.get('device_info'),
        })
        runtime.action_generate_api_key()

        return self._json_response({
            'status': 'ok',
            'runtime_id': runtime.id,
            'api_key': runtime.api_key,
        })

    @http.route(
        '/api/agent/<int:agent_id>/chat',
        type='http',
        methods=['POST'],
        auth='user',
        csrf=False,
    )
    def send_chat_message(self, agent_id, **kwargs):
        """Send a chat message to an agent (requires Odoo auth)."""
        content = kwargs.get('content')
        if not content:
            return self._json_response({'error': 'content required'}, 400)

        agent = request.env['odoo.agent'].sudo().browse(agent_id)
        if not agent.exists():
            return self._json_response({'error': 'Agent not found'}, 404)

        msg = request.env['odoo.agent.chat.message'].sudo().create({
            'agent_id': agent_id,
            'author_id': request.env.user.id,
            'author_type': 'user',
            'content': content,
        })

        return self._json_response({
            'status': 'ok',
            'message_id': msg.id,
            'agent_name': agent.name,
        })

    @http.route(
        '/api/agent/<int:agent_id>/chat/messages',
        type='http',
        methods=['GET'],
        auth='user',
        csrf=False,
    )
    def get_chat_messages(self, agent_id, **kwargs):
        """Get chat history with an agent."""
        agent = request.env['odoo.agent'].sudo().browse(agent_id)
        if not agent.exists():
            return self._json_response({'error': 'Agent not found'}, 404)

        limit = int(kwargs.get('limit', 50))
        messages = request.env['odoo.agent.chat.message'].sudo().search([
            ('agent_id', '=', agent_id),
        ], limit=limit)

        msg_data = []
        for msg in messages:
            msg_data.append({
                'id': msg.id,
                'author_type': msg.author_type,
                'author_name': msg.author_id.name if msg.author_id else 'Agent',
                'content': msg.content,
                'timestamp': str(msg.timestamp),
                'is_read': msg.is_read,
            })

        return self._json_response({'messages': msg_data})
