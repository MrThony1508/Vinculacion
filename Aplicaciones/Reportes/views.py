# Aplicaciones/Reportes/views.py
from django.shortcuts import render
from Aplicaciones.Docentes.models import Docente
from Aplicaciones.Estudiantes.models import Estudiante, Grupo
from django.db.models import Count, Q

def inicio4(request):
    """
    Vista de reportes académicos:
    - Total de estudiantes y grupos por docente
    - Total de estudiantes por carrera y tipo de práctica
    """

    # ============================
    # Reporte por docente
    # ============================
    docentes = Docente.objects.annotate(
        total_estudiantes=Count('estudiantes', distinct=True),
        total_grupos=Count('grupos', distinct=True)  # <-- aquí ya usamos related_name="grupos"
    )

    # ============================
    # Reporte por grupo
    # ============================
    grupos = Grupo.objects.annotate(
        total_estudiantes=Count('estudiantes')
    ).select_related('docente')

    # ============================
    # Reporte por carrera y tipo de práctica
    # ============================
    carreras = Estudiante.objects.values('carrera').annotate(
        total_estudiantes=Count('id'),
        ppp=Count('id', filter=Q(tipo_practica='PPP')),
        servicio_comunitario=Count('id', filter=Q(tipo_practica='Servicio Comunitario'))
    ).order_by('carrera')

    context = {
        'docentes': docentes,
        'grupos': grupos,
        'carreras': carreras
    }

    return render(request, "inicio4.html", context)
