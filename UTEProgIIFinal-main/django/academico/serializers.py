from rest_framework import serializers

from .models import Carrera, Estudiante, Matricula


class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = '__all__'


class EstudianteSerializer(serializers.ModelSerializer):
    carrera_nombre = serializers.CharField(source='carrera_id.name', read_only=True)
    modalidad = serializers.ReadOnlyField(source='modalidad')

    class Meta:
        model = Estudiante
        fields = '__all__'


class MatriculaSerializer(serializers.ModelSerializer):
    total = serializers.ReadOnlyField()

    class Meta:
        model = Matricula
        fields = '__all__'
