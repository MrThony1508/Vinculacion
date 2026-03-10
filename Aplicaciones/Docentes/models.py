from django.db import models
from django.contrib.auth.models import User

class Docente(models.Model):
    # Cambiamos a ForeignKey para permitir múltiples registros por usuario
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    
    # Quitamos unique=True porque el mismo docente aparecerá varias veces (una por periodo)
    cedula = models.CharField(max_length=10) 
    correo_institucional = models.EmailField()
    
    carrera = models.CharField(max_length=100)
    asignacion = models.CharField(max_length=100)
    periodo = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.periodo}"
class Programa(models.Model):
    # Asegúrate de que se llamen así:
    proyecto = models.CharField(max_length=255) 
    coordinador = models.CharField(max_length=255)
    periodo = models.CharField(max_length=100)
    estudiantes = models.IntegerField(default=0)

    def __str__(self):
        return self.proyecto
    
