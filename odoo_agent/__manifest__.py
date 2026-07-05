# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'AI Agent System',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'AI Agent management: runtimes, agents, skills, and tasks integrated with Odoo projects',
    'description': """
Replicates the Multica agent architecture natively within Odoo.
- Agent Runtimes: external machines (N100, Mac Mini, etc.) connected via API
- AI Agents: configurable entities with instructions, skills, and runtime assignment
- Agent Skills: reusable instruction packs
- Agent Tasks: tasks assigned to AI agents, linked to project.task
- REST API: bidirectional communication with external runtimes
    """,
    'author': 'Nicolas Ramos',
    'website': 'https://github.com/nicolasramos-es',
    'depends': ['project', 'mail', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'security/agent_security.xml',
        'views/agent_runtime_views.xml',
        'views/agent_views.xml',
        'views/agent_skill_views.xml',
        'views/agent_task_views.xml',
        'views/project_task_inherit_views.xml',
        'views/menu_views.xml',
        'data/agent_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
