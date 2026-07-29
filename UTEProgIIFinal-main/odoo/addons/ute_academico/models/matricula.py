from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UteMatricula(models.Model):
    _name = 'ute.matricula'
    _description = 'Matrícula'
    _order = 'id desc'

    name = fields.Char(string='Número de matrícula', required=True)
    estudiante_id = fields.Many2one('ute.estudiante', string='Estudiante', ondelete='cascade', required=True)
    periodo = fields.Selection([
        ('2026-01', '2026-01'),
        ('2026-02', '2026-02'),
    ], string='Periodo', required=True)
    asignatura = fields.Char(string='Asignatura', required=True)
    creditos = fields.Integer(string='Créditos', default=3)
    costo_credito = fields.Float(string='Costo por crédito', default=25.0)
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    fecha = fields.Date(string='Fecha', default=fields.Date.today)
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmada', 'Confirmada'),
        ('anulada', 'Anulada'),
    ], string='Estado', default='borrador', required=True)
    observacion = fields.Text(string='Observación')

    @api.depends('creditos', 'costo_credito')
    def _compute_total(self):
        for record in self:
            record.total = record.creditos * record.costo_credito

    @api.constrains('creditos')
    def _check_creditos(self):
        for record in self:
            if record.creditos < 1 or record.creditos > 6:
                raise ValidationError('Los créditos deben estar entre 1 y 6.')

    def action_confirmar(self):
        for record in self:
            if record.estado == 'anulada':
                raise ValidationError('No se puede volver atrás desde una matrícula anulada.')
            if record.estado != 'borrador':
                raise ValidationError('Solo se pueden confirmar matrículas en borrador.')
            record.estado = 'confirmada'
        return True

    def action_anular(self):
        for record in self:
            if record.estado == 'anulada':
                raise ValidationError('La matrícula ya está anulada.')
            record.estado = 'anulada'
        return True
