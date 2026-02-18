from django.shortcuts import render
from Aplicaciones.Estudiantes.models import Estudiante

def inicio2(request):
    estudiantes_qs = Estudiante.objects.filter(
        grupo__latitud__isnull=False,
        grupo__longitud__isnull=False
    ).values(
        'nombre', 'apellido', 'carrera', 'tipo_practica', 'semestre', 
        'periodo_academico', # Nombre correcto según tu error
        'grupo__nombre', 'grupo__latitud', 'grupo__longitud',
        'docente__nombre', 'docente__apellido'
    )

    estudiantes_lista = []
    for e in estudiantes_qs:
        estudiantes_lista.append({
            'nombre': e['nombre'],
            'apellido': e['apellido'],
            'carrera': e['carrera'],
            'tipo_practica': e['tipo_practica'],
            'semestre': e['semestre'],
            'periodo': e['periodo_academico'], # Lo guardamos como 'periodo' para el JS
            'grupo_nombre': e['grupo__nombre'],
            'lat': float(e['grupo__latitud']),
            'lng': float(e['grupo__longitud']),
            'docente': f"{e['docente__nombre']} {e['docente__apellido']}"
        })

    return render(request, 'inicio2.html', {
        'estudiantes': estudiantes_lista
    })