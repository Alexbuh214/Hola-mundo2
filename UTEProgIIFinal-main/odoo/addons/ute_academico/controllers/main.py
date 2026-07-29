from odoo import http, fields
from odoo.http import request


class AcademicoController(http.Controller):

    @http.route('/academico/ping', type='http', auth='public')
    def ping(self, **kw):
        return request.make_json_response({
            'mensaje': 'El controlador responde correctamente',
            'fecha': fields.Date.today(),
        })

    @http.route('/academico/api/carreras', type='http', auth='public', csrf=False)
    def api_carreras(self, **kw):
        carreras = request.env['ute.carrera'].sudo().search([('activa', '=', True)])
        data = [{
            'id': carrera.id,
            'name': carrera.name,
            'codigo': carrera.codigo,
            'modalidad': carrera.modalidad,
        } for carrera in carreras]
        return request.make_json_response(data)

    @http.route('/academico/api/estudiantes', type='http', auth='public', csrf=False)
    def api_estudiantes(self, **kw):
        estudiantes = request.env['ute.estudiante'].sudo().search([('estado', '=', 'activo')])
        data = [{
            'id': estudiante.id,
            'name': estudiante.name,
            'cedula': estudiante.cedula,
            'carrera': estudiante.carrera_id.name if estudiante.carrera_id else False,
            'estado': estudiante.estado,
        } for estudiante in estudiantes]
        return request.make_json_response(data)

    @http.route('/academico/api/estudiante/<int:estudiante_id>', type='http', auth='public', csrf=False)
    def api_estudiante(self, estudiante_id, **kw):
        estudiante = request.env['ute.estudiante'].sudo().browse(estudiante_id)
        if not estudiante.exists():
            return request.make_json_response({'error': 'Estudiante no encontrado.'}, status=404)

        data = {
            'id': estudiante.id,
            'name': estudiante.name,
            'cedula': estudiante.cedula,
            'email': estudiante.email,
            'estado': estudiante.estado,
            'carrera': estudiante.carrera_id.name if estudiante.carrera_id else False,
            'matriculas': [{
                'id': matricula.id,
                'name': matricula.name,
                'periodo': matricula.periodo,
                'asignatura': matricula.asignatura,
                'estado': matricula.estado,
            } for matricula in estudiante.matricula_ids],
        }
        return request.make_json_response(data)
