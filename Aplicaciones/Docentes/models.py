from django.db import models
from django.contrib.auth.models import User

class Docente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    correo_institucional = models.EmailField(unique=True)
    carrera = models.CharField(max_length=100)
    asignacion = models.CharField(max_length=100)  # ← igual que carrera

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
