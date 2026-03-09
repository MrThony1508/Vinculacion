from django.shortcuts import render
from django.db.models import Count, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce
from Aplicaciones.Docentes.models import Programa
from Aplicaciones.Estudiantes.models import  Estudiante

def inicio3(request):
    # Subconsulta eficiente para contar estudiantes asociados a cada proyecto
    conteo_subquery = Estudiante.objects.filter(
        proyecto=OuterRef('proyecto')
    ).values('proyecto').annotate(total=Count('id')).values('total')

    # Obtenemos los programas y les asignamos el conteo real
    programas = Programa.objects.annotate(
        conteo_real=Coalesce(Subquery(conteo_subquery), 0, output_field=IntegerField())
    ).order_by('-id')

    return render(request, "inicio3.html", {'programas': programas})