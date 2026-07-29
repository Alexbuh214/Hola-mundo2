from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets

from .models import Carrera, Estudiante, Matricula
from .serializers import CarreraSerializer, EstudianteSerializer, MatriculaSerializer


def estudiantes_list(request):
    estudiantes = Estudiante.objects.select_related('carrera_id').all()
    return render(request, 'academico/estudiantes_list.html', {'estudiantes': estudiantes})


def estudiante_detail(request, pk):
    estudiante = get_object_or_404(Estudiante.objects.select_related('carrera_id'), pk=pk)
    matriculas = estudiante.matriculas.all()
    return render(request, 'academico/estudiante_detail.html', {'estudiante': estudiante, 'matriculas': matriculas})


class CarreraViewSet(viewsets.ModelViewSet):
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer


class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.select_related('carrera_id').all()
    serializer_class = EstudianteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        carrera = self.request.query_params.get('carrera')
        if carrera:
            queryset = queryset.filter(carrera_id=carrera)
        return queryset


class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.select_related('estudiante_id').all()
    serializer_class = MatriculaSerializer
