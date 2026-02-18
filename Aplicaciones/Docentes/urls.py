from django.urls import path
from . import views

urlpatterns = [
    path('docentes/', views.lista_docentes, name='lista_docentes'),
    path('docentes/nuevo/', views.nuevo_docente, name='nuevo_docente'),
    path('docentes/guardar/', views.guardar_docente, name='guardar_docente'),
    path('docentes/editar/<int:id>/', views.editar_docente, name='editar_docente'),
    path('docentes/actualizar/', views.procesar_edicion_docente, name='procesar_edicion_docente'),
    path('docentes/eliminar/<int:id>/', views.eliminar_docente, name='eliminar_docente'),
    path('validar_cedula_unica/', views.validar_cedula_unica, name='validar_cedula_unica'),
    path('validar_correo_unico/', views.validar_correo_unico, name='validar_correo_unico'),

    #Programa
    path('programas/', views.lista_programas, name='lista_programas'),
    path('programas/nuevo/', views.nuevo_programa, name='nuevo_programa'),
    path('programas/guardar/', views.guardar_programa, name='guardar_programa'),
    path('programas/editar/<int:id>/', views.editar_programa, name='editar_programa'),
    path('programas/actualizar/', views.procesar_edicion_programa, name='procesar_edicion_programa'),
    path('programas/eliminar/<int:id>/', views.eliminar_programa, name='eliminar_programa'),
]
