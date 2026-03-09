from django.shortcuts import render
from Aplicaciones.Estudiantes.models import Estudiante

def inicio2(request):
    # Consultamos los estudiantes que tengan coordenadas
    estudiantes_qs = Estudiante.objects.filter(
        grupo__latitud__isnull=False,
        grupo__longitud__isnull=False
    ).values(
        'nombre', 'apellido', 'carrera', 'tipo_practica', 'semestre', 
        'periodo_academico', 
        'grupo__nombre', 'grupo__latitud', 'grupo__longitud',
        'docente__nombre', 'docente__apellido'
    )

    # Obtenemos los periodos únicos para llenar el select del filtro
    periodos = Estudiante.objects.values_list('periodo_academico', flat=True).distinct().order_by('-periodo_academico')

    estudiantes_lista = []
    for e in estudiantes_qs:
        estudiantes_lista.append({
            'nombre': e['nombre'],
            'apellido': e['apellido'],
            'carrera': e['carrera'],
            'tipo_practica': e['tipo_practica'],
            'semestre': e['semestre'],
            'periodo': e['periodo_academico'], 
            'grupo_nombre': e['grupo__nombre'],
            'lat': float(e['grupo__latitud']),
            'lng': float(e['grupo__longitud']),
            'docente': f"{e['docente__nombre']} {e['docente__apellido']}"
        })

    return render(request, 'inicio2.html', {
        'estudiantes': estudiantes_lista,
        'periodos': periodos
    })