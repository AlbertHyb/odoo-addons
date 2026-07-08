# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json

from odoo.tests import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestAgentRuntimeApi(HttpCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.runtime = cls.env['odoo.agent.runtime'].create({
            'name': 'API Runtime',
            'machine_id': 'api-runtime',
            'company_id': cls.company.id,
        })
        cls.runtime.action_generate_api_key()
        cls.other_runtime = cls.env['odoo.agent.runtime'].create({
            'name': 'Other API Runtime',
            'machine_id': 'other-api-runtime',
            'company_id': cls.company.id,
        })
        cls.other_runtime.action_generate_api_key()
        cls.agent = cls.env['odoo.agent'].create({
            'name': 'API Agent',
            'runtime_id': cls.runtime.id,
            'engine': 'opencode',
            'cli_command': 'opencode run --instruction {instruction}',
            'company_id': cls.company.id,
        })
        cls.execution = cls.env['odoo.agent.execution'].create({
            'name': 'API Execution',
            'prompt': 'API prompt',
            'agent_id': cls.agent.id,
            'runtime_id': cls.runtime.id,
            'company_id': cls.company.id,
        })

    def _json_request(self, path, api_key=None, payload=None):
        headers = {'Content-Type': 'application/json'}
        if api_key:
            headers['X-API-Key'] = api_key
        response = self.url_open(
            path,
            data=json.dumps(payload or {}).encode(),
            headers=headers,
        )
        return response.status_code, json.loads(response.read().decode())

    def test_heartbeat_requires_valid_api_key(self):
        status, payload = self._json_request('/api/agent/runtime/heartbeat', api_key='invalid')

        self.assertEqual(status, 401)
        self.assertEqual(payload['code'], 'invalid_api_key')

    def test_poll_returns_owned_execution_payload(self):
        status, payload = self._json_request(
            '/api/agent/runtime/poll',
            api_key=self.runtime.api_key,
            payload={'limit': 5},
        )

        self.assertEqual(status, 200)
        self.assertEqual(payload['status'], 'ok')
        self.assertEqual(payload['executions'][0]['id'], self.execution.id)
        self.assertEqual(payload['executions'][0]['agent']['engine'], 'opencode')

    def test_cross_runtime_start_is_denied(self):
        status, payload = self._json_request(
            f'/api/agent/execution/{self.execution.id}/start',
            api_key=self.other_runtime.api_key,
        )

        self.assertEqual(status, 403)
        self.assertEqual(payload['code'], 'forbidden')

    def test_log_requires_message(self):
        status, payload = self._json_request(
            f'/api/agent/execution/{self.execution.id}/log',
            api_key=self.runtime.api_key,
            payload={'level': 'info'},
        )

        self.assertEqual(status, 400)
        self.assertEqual(payload['code'], 'validation_error')
