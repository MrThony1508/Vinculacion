from django.shortcuts import render
from Aplicaciones.Docentes.models import Programa # Importa tu modelo Programa

def inicio3(request):
    # Obtenemos todos los programas registrados en la base de datos
    programas_db = Programa.objects.all()
    # Los enviamos al template bajo el nombre 'programas'
    return render(request, "inicio3.html", {'programas': programas_db})