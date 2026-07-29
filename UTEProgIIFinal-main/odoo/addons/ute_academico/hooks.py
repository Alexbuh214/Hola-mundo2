from odoo import SUPERUSER_ID


def post_init_hook(env, **kwargs):
    model_names = ['ute.carrera', 'ute.estudiante', 'ute.matricula']
    for model_name in model_names:
        model = env['ir.model'].search([('model', '=', model_name)])
        if model:
            existing = env['ir.model.access'].search([
                ('name', '=', f'access_{model_name.replace(".", "_")}'),
                ('model_id', '=', model.id),
            ])
            if not existing:
                env['ir.model.access'].create({
                    'name': f'access_{model_name.replace(".", "_")}',
                    'model_id': model.id,
                    'group_id': env.ref('base.group_user').id,
                    'perm_read': True,
                    'perm_write': True,
                    'perm_create': True,
                    'perm_unlink': True,
                })
