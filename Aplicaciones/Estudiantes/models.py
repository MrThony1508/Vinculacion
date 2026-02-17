from django.db import models
from Aplicaciones.Docentes.models import Docente

class Grupo(models.Model):
    docente = models.ForeignKey(
        Docente,
        on_delete=models.CASCADE,
        related_name="grupos"
    )

    numero = models.PositiveIntegerField()
    nombre = models.CharField(max_length=100, blank=True)

    actividades_realizadas = models.TextField()
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.nombre:
            self.nombre = f"Grupo {self.numero}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Estudiante(models.Model):
    docente = models.ForeignKey(
        Docente,
        on_delete=models.CASCADE,
        related_name='estudiantes'
    )

    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='estudiantes'
    )

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10)
    correo_institucional = models.EmailField(max_length=100)

    carrera = models.CharField(max_length=100)
    tipo_practica = models.CharField(max_length=50)
    semestre = models.CharField(max_length=50)
    periodo_academico = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
