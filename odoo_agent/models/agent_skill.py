# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AgentSkill(models.Model):
    _name = 'odoo.agent.skill'
    _description = 'Agent Skill'
    _order = 'category, name, id'

    name = fields.Char(string='Name', required=True, index=True)
    description = fields.Text(string='Description')
    instructions = fields.Text(
        string='Instructions',
        required=True,
        help='The skill instructions/prompt that will be injected into the agent',
    )
    category = fields.Selection(
        [
            ('development', 'Development'),
            ('devops', 'DevOps'),
            ('analysis', 'Analysis'),
            ('communication', 'Communication'),
            ('custom', 'Custom'),
        ],
        string='Category',
        default='custom',
        required=True,
    )
    agent_ids = fields.Many2many(
        'odoo.agent',
        'agent_skill_rel',
        'skill_id',
        'agent_id',
        string='Agents',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(string='Active', default=True)
