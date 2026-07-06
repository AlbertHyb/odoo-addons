# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AgentLog(models.Model):
    _name = 'odoo.agent.log'
    _description = 'Agent Task Log'
    _order = 'timestamp desc, id'
    _rec_name = 'message'

    agent_task_id = fields.Many2one(
        'odoo.agent.task',
        string='Agent Task',
        required=True,
        ondelete='cascade',
        index=True,
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

    @api.model
    def add_log(self, task_id, level, message, command=None, exit_code=None):
        """Add a log entry for a task."""
        return self.create({
            'agent_task_id': task_id,
            'level': level,
            'message': message,
            'command': command,
            'exit_code': exit_code,
            'timestamp': fields.Datetime.now(),
        })

    @api.model
    def get_task_logs(self, task_id, level=None, limit=100):
        """Get logs for a specific task."""
        domain = [('agent_task_id', '=', task_id)]
        if level:
            domain.append(('level', '=', level))
        return self.search(domain, limit=limit)
