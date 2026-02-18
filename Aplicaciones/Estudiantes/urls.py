from django.urls import path
from . import views

urlpatterns = [
    # Estudiantes
    path('estudiantes/', views.lista_estudiantes, name='lista_estudiantes'),
    path('estudiantes/nuevo/', views.nuevo_estudiante, name='nuevo_estudiante'),
    path('estudiantes/guardar/', views.guardar_estudiante, name='guardar_estudiante'),
    path('estudiantes/editar/<int:id>/', views.editar_estudiante, name='editar_estudiante'),
    path('estudiantes/actualizar/', views.procesar_edicion_estudiante, name='procesar_edicion_estudiante'),
    path('estudiantes/eliminar/<int:id>/', views.eliminar_estudiante, name='eliminar_estudiante'),
    path('estudiantes/remover_grupo/<int:id>/', views.remover_estudiante_grupo, name='remover_estudiante_grupo'),
    path('validar-cedula-estudiante/', views.validar_cedula_estudiante_unica, name='validar_cedula_estudiante'),
    path('validar-correo-estudiante/', views.validar_correo_estudiante_unico, name='validar_correo_estudiante'),

    # Grupos
    path('grupos/', views.lista_grupos, name='lista_grupos'),
    path('grupos/crear/', views.crear_grupo, name='crear_grupo'),
    path('grupos/guardar/', views.guardar_grupo, name='guardar_grupo'),
    path('grupos/eliminar/<int:id>/', views.eliminar_grupo, name='eliminar_grupo'),
    path('grupos/<int:grupo_id>/', views.detalle_grupo, name='detalle_grupo'),
    path('grupos/<int:grupo_id>/asignar/', views.asignar_estudiantes, name='asignar_estudiantes'),
]
