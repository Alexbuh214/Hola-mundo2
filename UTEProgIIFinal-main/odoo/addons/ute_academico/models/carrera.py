from datetime import date

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UteCarrera(models.Model):
    _name = 'ute.carrera'
    _description = 'Carrera'
    _order = 'name'

    name = fields.Char(string='Carrera', required=True)
    codigo = fields.Char(string='Código', required=True)
    modalidad = fields.Selection([
        ('presencial', 'Presencial'),
        ('semipresencial', 'Semipresencial'),
        ('online', 'Online'),
    ], string='Modalidad', default='presencial', required=True)
    duracion_semestres = fields.Integer(string='Duración en semestres', default=8)
    cupo_maximo = fields.Integer(string='Cupo máximo', default=40)
    activa = fields.Boolean(string='Activa', default=True)
    estudiante_ids = fields.One2many('ute.estudiante', 'carrera_id', string='Estudiantes')
    total_estudiantes = fields.Integer(
        string='Total estudiantes',
        compute='_compute_total_estudiantes',
        store=True,
    )

    _sql_constraints = [
        ('codigo_uniq', 'unique(codigo)', 'El código de la carrera ya existe.'),
    ]

    @api.depends('estudiante_ids', 'estudiante_ids.estado')
    def _compute_total_estudiantes(self):
        for record in self:
            record.total_estudiantes = len(record.estudiante_ids.filtered(lambda e: e.estado == 'activo'))

    @api.constrains('duracion_semestres')
    def _check_duracion_semestres(self):
        for record in self:
            if record.duracion_semestres < 4 or record.duracion_semestres > 12:
                raise ValidationError('La duración en semestres debe estar entre 4 y 12.')

    @api.constrains('cupo_maximo')
    def _check_cupo_maximo(self):
        for record in self:
            if record.cupo_maximo <= 0:
                raise ValidationError('El cupo máximo debe ser mayor que 0.')
