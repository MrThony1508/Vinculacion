from django.shortcuts import render
from Aplicaciones.Estudiantes.models import Estudiante

def inicio2(request):
    estudiantes = Estudiante.objects.filter(
        grupo__latitud__isnull=False,
        grupo__longitud__isnull=False
    ).values(
        'nombre',
        'apellido',
        'carrera',
        'tipo_practica',
        'grupo__nombre',
        'grupo__latitud',
        'grupo__longitud'
    )

    return render(request, 'inicio2.html', {
        'estudiantes': list(estudiantes)
    })
