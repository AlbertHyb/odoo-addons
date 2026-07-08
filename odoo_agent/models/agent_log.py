# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AgentLog(models.Model):
    _name = 'odoo.agent.log'
    _description = 'Agent Execution Log'
    _order = 'timestamp desc, id'
    _rec_name = 'message'
    _check_company_auto = True

    execution_id = fields.Many2one(
        'odoo.agent.execution',
        string='Execution',
        ondelete='cascade',
        index=True,
        check_company=True,
    )
    agent_task_id = fields.Many2one(
        'odoo.agent.task',
        string='Legacy Agent Task',
        ondelete='cascade',
        index=True,
    )
    runtime_id = fields.Many2one(
        related='execution_id.runtime_id',
        store=True,
        readonly=True,
        string='Runtime',
    )
    agent_id = fields.Many2one(
        related='execution_id.agent_id',
        store=True,
        readonly=True,
        string='Agent',
    )
    timestamp = fields.Datetime(
        string='Timestamp',
        required=True,
        default=fields.Datetime.now,
        index=True,
    )
    level = fields.Selection(
        [
            ('debug', 'DEBUG'),
            ('info', 'INFO'),
            ('warn', 'WARNING'),
            ('error', 'ERROR'),
        ],
        string='Level',
        default='info',
        required=True,
        index=True,
    )
    message = fields.Text(string='Message', required=True)
    command = fields.Text(string='Command', help='The command/action being executed')
    exit_code = fields.Integer(string='Exit Code')
    company_id = fields.Many2one(
        related='execution_id.company_id',
        store=True,
        readonly=True,
        string='Company',
    )

    @api.model_create_multi
    def create(self, vals_list):
        logs = super().create(vals_list)
        for log in logs:
            log._notify_log_event()
        return logs

    @api.model
    def add_log(self, execution_id, level, message, command=None, exit_code=None):
        return self.create({
            'execution_id': execution_id,
            'level': level,
            'message': message,
            'command': command,
            'exit_code': exit_code,
            'timestamp': fields.Datetime.now(),
        })

    @api.model
    def get_execution_logs(self, execution_id, level=None, limit=100):
        domain = [('execution_id', '=', execution_id)]
        if level:
            domain.append(('level', '=', level))
        return self.search(domain, limit=limit)

    @api.model
    def get_task_logs(self, task_id, level=None, limit=100):
        domain = ['|', ('agent_task_id', '=', task_id), ('execution_id.task_id', '=', task_id)]
        if level:
            domain.append(('level', '=', level))
        return self.search(domain, limit=limit)

    def _notify_log_event(self):
        self.ensure_one()
        if not self.execution_id:
            return
        payload = {
            'event': 'log_created',
            'log_id': self.id,
            'execution_id': self.execution_id.id,
            'agent_id': self.execution_id.agent_id.id,
            'runtime_id': self.execution_id.runtime_id.id,
            'level': self.level,
            'message': self.message,
            'timestamp': fields.Datetime.to_string(self.timestamp) if self.timestamp else None,
        }
        self.env['bus.bus']._sendone(
            f'odoo_agent.execution.{self.execution_id.id}',
            'odoo_agent',
            payload,
        )
        self.env['bus.bus']._sendone(
            f'odoo_agent.agent.{self.execution_id.agent_id.id}',
            'odoo_agent',
            payload,
        )
        if self.execution_id.task_id:
            self.env['bus.bus']._sendone(
                f'odoo_agent.project_task.{self.execution_id.task_id.id}',
                'odoo_agent',
                payload,
            )
