# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import secrets


class AgentRuntime(models.Model):
    _name = 'odoo.agent.runtime'
    _description = 'AI Agent Runtime'
    _order = 'name, id'

    name = fields.Char(string='Name', required=True, index=True)
    machine_id = fields.Char(
        string='Machine ID',
        required=True,
        index=True,
        help='Unique machine identifier (hostname or UUID)',
    )
    ip_address = fields.Char(string='IP Address')
    status = fields.Selection(
        [
            ('offline', 'Offline'),
            ('online', 'Online'),
            ('busy', 'Busy'),
        ],
        string='Status',
        default='offline',
        required=True,
        index=True,
    )
    last_seen = fields.Datetime(string='Last Seen')
    api_key = fields.Char(
        string='API Key',
        help='API key for runtime authentication',
        groups='odoo_agent.group_agent_admin',
    )
    version = fields.Char(string='Version', help='Daemon/CLI version')
    device_info = fields.Char(string='Device Info', help='OS, hardware info')
    agent_ids = fields.One2many(
        'odoo.agent', 'runtime_id', string='Agents',
    )
    active_agent_count = fields.Integer(
        string='Active Agents',
        compute='_compute_active_agent_count',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    _sql_constraints = [
        (
            'machine_id_unique',
            'unique(machine_id, company_id)',
            'Machine ID must be unique per company.',
        ),
    ]

    @api.depends('agent_ids', 'agent_ids.status')
    def _compute_active_agent_count(self):
        for runtime in self:
            runtime.active_agent_count = len(
                runtime.agent_ids.filtered(lambda a: a.status == 'working')
            )

    def action_generate_api_key(self):
        """Generate a new API key for this runtime."""
        self.ensure_one()
        self.api_key = secrets.token_urlsafe(32)

    def action_mark_online(self):
        self.status = 'online'
        self.last_seen = fields.Datetime.now()

    def action_mark_offline(self):
        self.status = 'offline'
        for agent in self.agent_ids:
            if agent.status == 'working':
                agent.status = 'error'
