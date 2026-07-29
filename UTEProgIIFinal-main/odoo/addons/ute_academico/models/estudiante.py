import re
from datetime import date

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UteEstudiante(models.Model):
    _name = 'ute.estudiante'
    _description = 'Estudiante'
    _order = 'name'

    name = fields.Char(string='Nombres y apellidos', required=True)
    cedula = fields.Char(string='Cédula', required=True)
    email = fields.Char(string='Correo electrónico')
    telefono = fields.Char(string='Teléfono')
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento')
    edad = fields.Integer(string='Edad', compute='_compute_edad', store=False)
    genero = fields.Selection([
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ], string='Género', required=True)
    carrera_id = fields.Many2one('ute.carrera', string='Carrera', ondelete='restrict', required=True)
    modalidad = fields.Selection(related='carrera_id.modalidad', string='Modalidad', readonly=True, store=False)
    fecha_ingreso = fields.Date(string='Fecha de ingreso', default=fields.Date.today)
    estado = fields.Selection([
        ('activo', 'Activo'),
        ('egresado', 'Egresado'),
        ('retirado', 'Retirado'),
    ], string='Estado', default='activo', required=True)
    matricula_ids = fields.One2many('ute.matricula', 'estudiante_id', string='Matrículas')
    notas = fields.Text(string='Notas')

    _sql_constraints = [
        ('cedula_uniq', 'unique(cedula)', 'La cédula ya está registrada.'),
    ]

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        today = date.today()
        for record in self:
            if not record.fecha_nacimiento:
                record.edad = 0
            else:
                record.edad = today.year - record.fecha_nacimiento.year - ((today.month, today.day) < (record.fecha_nacimiento.month, record.fecha_nacimiento.day))

    @api.constrains('cedula')
    def _check_cedula(self):
        for record in self:
            if not re.fullmatch(r'\d{10}', record.cedula or ''):
                raise ValidationError('La cédula debe tener exactamente 10 dígitos numéricos.')

    @api.constrains('fecha_nacimiento')
    def _check_fecha_nacimiento(self):
        for record in self:
            if record.fecha_nacimiento and record.fecha_nacimiento > date.today():
                raise ValidationError('La fecha de nacimiento no puede ser futura.')
