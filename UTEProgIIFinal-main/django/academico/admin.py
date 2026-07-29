from django.contrib import admin

from .models import Carrera, Estudiante, Matricula


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('name', 'codigo', 'modalidad', 'duracion_semestres', 'cupo_maximo', 'activa')
    search_fields = ('name', 'codigo')


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('name', 'cedula', 'carrera_id', 'estado', 'fecha_ingreso')
    search_fields = ('name', 'cedula')


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('name', 'estudiante_id', 'periodo', 'asignatura', 'creditos', 'estado')
    search_fields = ('name', 'asignatura', 'estudiante_id__name')
