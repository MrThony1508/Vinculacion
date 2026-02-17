from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Perfil  # Importamos Docente
from django.db.models import Count    # Para agrupar por carrera
from datetime import date             # Para filtrar los de hoy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from Aplicaciones.Docentes.models import Docente

# Tu lógica de Login se mantiene igual...
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('dashboard')
            try:
                perfil = Perfil.objects.get(user=user)
                if perfil.rol == 'docente':
                    return redirect('lista_estudiantes')
            except Perfil.DoesNotExist:
                pass
            messages.error(request, 'Rol no válido')
            logout(request)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# Tu función dashboard con la visualización conectada
@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Acceso denegado")
    
    # --- LOGICA PARA VISUALIZACIÓN ---
    total_docentes = Docente.objects.count()
    nuevos_hoy = Docente.objects.filter(user__date_joined__date=date.today()).count()
    # Obtenemos cuántos docentes hay por cada carrera registrada
    docentes_por_carrera = Docente.objects.values('carrera').annotate(total=Count('carrera')).order_by('-total')

    return render(request, 'dashboard.html', {
        'total_docentes': total_docentes,
        'nuevos_hoy': nuevos_hoy,
        'docentes_por_carrera': docentes_por_carrera,
    })