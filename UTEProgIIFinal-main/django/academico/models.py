from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class Carrera(models.Model):
    MODALIDAD_CHOICES = [
        ('presencial', 'Presencial'),
        ('semipresencial', 'Semipresencial'),
        ('online', 'Online'),
    ]

    name = models.CharField(max_length=100, verbose_name='Carrera')
    codigo = models.CharField(max_length=6, unique=True, verbose_name='Código')
    modalidad = models.CharField(max_length=20, choices=MODALIDAD_CHOICES, verbose_name='Modalidad')
    duracion_semestres = models.PositiveSmallIntegerField(default=8, verbose_name='Duración en semestres')
    cupo_maximo = models.PositiveIntegerField(default=40, verbose_name='Cupo máximo')
    activa = models.BooleanField(default=True, verbose_name='Activa')

    class Meta:
        ordering = ['name']
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'

    def __str__(self):
        return self.name

    @property
    def total_estudiantes(self):
        return self.estudiantes.filter(estado='activo').count()


class Estudiante(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('egresado', 'Egresado'),
        ('retirado', 'Retirado'),
    ]

    name = models.CharField(max_length=120, verbose_name='Nombres y apellidos')
    cedula = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message='La cédula debe tener exactamente 10 dígitos numéricos')],
        verbose_name='Cédula',
    )
    email = models.EmailField(blank=True, verbose_name='Correo electrónico')
    telefono = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, verbose_name='Género')
    carrera_id = models.ForeignKey('academico.Carrera', on_delete=models.PROTECT, related_name='estudiantes', verbose_name='Carrera')
    fecha_ingreso = models.DateField(default=date.today, verbose_name='Fecha de ingreso')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo', verbose_name='Estado')
    notas = models.TextField(blank=True, verbose_name='Notas')

    class Meta:
        ordering = ['name']
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return self.name

    @property
    def edad(self):
        if not self.fecha_nacimiento:
            return None
        today = date.today()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    @property
    def modalidad(self):
        return self.carrera_id.modalidad if self.carrera_id else None

    def clean(self):
        super().clean()
        if self.fecha_nacimiento and self.fecha_nacimiento > date.today():
            raise ValidationError({'fecha_nacimiento': 'La fecha de nacimiento no puede ser futura'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Matricula(models.Model):
    PERIODO_CHOICES = [
        ('2026-01', '2026-01'),
        ('2026-02', '2026-02'),
    ]
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('confirmada', 'Confirmada'),
        ('anulada', 'Anulada'),
    ]

    name = models.CharField(max_length=20, verbose_name='Número de matrícula')
    estudiante_id = models.ForeignKey('academico.Estudiante', on_delete=models.CASCADE, related_name='matriculas', verbose_name='Estudiante')
    periodo = models.CharField(max_length=7, choices=PERIODO_CHOICES, verbose_name='Periodo')
    asignatura = models.CharField(max_length=100, verbose_name='Asignatura')
    creditos = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(6)], verbose_name='Créditos')
    costo_credito = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('25.00'), verbose_name='Costo por crédito')
    fecha = models.DateField(default=date.today, verbose_name='Fecha')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador', verbose_name='Estado')
    observacion = models.TextField(blank=True, verbose_name='Observación')

    class Meta:
        ordering = ['-fecha', '-id']
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'

    def __str__(self):
        return self.name

    @property
    def total(self):
        return self.creditos * self.costo_credito

    def clean(self):
        super().clean()
        if self.creditos < 1 or self.creditos > 6:
            raise ValidationError({'creditos': 'Los créditos deben estar entre 1 y 6'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def action_confirmar(self):
        if self.estado == 'anulada':
            raise ValidationError('No se puede volver atrás desde una matrícula anulada')
        self.estado = 'confirmada'
        self.save(update_fields=['estado'])
        return self.estado

    def action_anular(self):
        if self.estado == 'borrador':
            self.estado = 'anulada'
            self.save(update_fields=['estado'])
            return self.estado
        if self.estado == 'confirmada':
            self.estado = 'anulada'
            self.save(update_fields=['estado'])
            return self.estado
        raise ValidationError('La matrícula ya está anulada')
