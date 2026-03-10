import csv
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce
from Aplicaciones.Docentes.models import Programa
from Aplicaciones.Estudiantes.models import Estudiante

def inicio3(request):
    conteo_subquery = Estudiante.objects.filter(
        proyecto=OuterRef('proyecto')
    ).values('proyecto').annotate(total=Count('id')).values('total')

    programas = Programa.objects.annotate(
        conteo_real=Coalesce(Subquery(conteo_subquery), 0, output_field=IntegerField())
    ).order_by('-id')

    return render(request, "inicio3.html", {'programas': programas})

def descargar_estudiantes(request, proyecto):
    # Crear respuesta HTTP con el tipo de contenido para CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="estudiantes_{proyecto}.csv"'

    writer = csv.writer(response)
    # Encabezados
    writer.writerow(['Apellido', 'Nombre', 'Correo', 'Carrera', 'Periodo Académico'])

    # Filtrar estudiantes por el nombre del proyecto
    estudiantes = Estudiante.objects.filter(proyecto=proyecto)

    for est in estudiantes:
        # Usamos los nombres exactos definidos en tu clase Estudiante
        writer.writerow([
            est.apellido, 
            est.nombre, 
            est.correo_institucional, 
            est.carrera, 
            est.periodo_academico
        ])

    return response