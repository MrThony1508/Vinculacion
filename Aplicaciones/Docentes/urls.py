from django.urls import path
from . import views

urlpatterns = [
    path('docentes/', views.lista_docentes, name='lista_docentes'),
    path('docentes/nuevo/', views.nuevo_docente, name='nuevo_docente'),
    path('docentes/guardar/', views.guardar_docente, name='guardar_docente'),
    path('docentes/editar/<int:id>/', views.editar_docente, name='editar_docente'),
    path('docentes/actualizar/', views.procesar_edicion_docente, name='procesar_edicion_docente'),
    path('docentes/eliminar/<int:id>/', views.eliminar_docente, name='eliminar_docente'),
]
