from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CarreraViewSet,
    EstudianteViewSet,
    MatriculaViewSet,
    estudiantes_list,
    estudiante_detail,
)

router = DefaultRouter()
router.register(r'carreras', CarreraViewSet, basename='carrera')
router.register(r'estudiantes', EstudianteViewSet, basename='estudiante')
router.register(r'matriculas', MatriculaViewSet, basename='matricula')

urlpatterns = [
    path('estudiantes/', estudiantes_list, name='estudiantes_list'),
    path('estudiantes/<int:pk>/', estudiante_detail, name='estudiante_detail'),
    path('api/', include(router.urls)),
]
