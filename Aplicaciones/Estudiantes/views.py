from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from Aplicaciones.Docentes.models import Docente
from .models import Estudiante, Grupo

# ============================
# LISTADO DE ESTUDIANTES
# ============================
@login_required
def lista_estudiantes(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'docente':
        return HttpResponseForbidden("Acceso denegado")

    docente = get_object_or_404(Docente, user=request.user)
    estudiantes = Estudiante.objects.filter(docente=docente)

    return render(request, 'lista_estudiantes.html', {'estudiantes': estudiantes})


# ============================
# NUEVO ESTUDIANTE
# ============================
@login_required
def nuevo_estudiante(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'docente':
        return HttpResponseForbidden("Acceso denegado")

    return render(request, 'estudiante_form.html')


# ============================
# GUARDAR ESTUDIANTE
# ============================
@login_required
def guardar_estudiante(request):
    if request.method == 'POST':
        docente = get_object_or_404(Docente, user=request.user)

        Estudiante.objects.create(
            docente=docente,
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            cedula=request.POST.get('cedula'),
            correo_institucional=request.POST.get('correo_institucional'),
            carrera=request.POST.get('carrera'),
            tipo_practica=request.POST.get('tipo_practica'),
            semestre=request.POST.get('semestre'),
            periodo_academico=request.POST.get('periodo_academico'),
        )

        messages.success(request, 'Estudiante registrado correctamente')
        return redirect('lista_estudiantes')

    return redirect('nuevo_estudiante')


# ============================
# ELIMINAR ESTUDIANTE
# ============================
@login_required
def eliminar_estudiante(request, id):
    docente = get_object_or_404(Docente, user=request.user)
    estudiante = get_object_or_404(Estudiante, id=id, docente=docente)

    estudiante.delete()
    messages.success(request, 'Estudiante eliminado correctamente')
    return redirect('lista_estudiantes')


# ============================
# EDITAR ESTUDIANTE
# ============================
@login_required
def editar_estudiante(request, id):
    docente = get_object_or_404(Docente, user=request.user)
    estudiante = get_object_or_404(Estudiante, id=id, docente=docente)

    return render(request, 'estudiante_editar.html', {'estudiante': estudiante})


# ============================
# PROCESAR EDICIÓN ESTUDIANTE
# ============================
@login_required
def procesar_edicion_estudiante(request):
    if request.method == 'POST':
        estudiante = get_object_or_404(Estudiante, id=request.POST.get('id'))

        estudiante.nombre = request.POST.get('nombre')
        estudiante.apellido = request.POST.get('apellido')
        estudiante.cedula = request.POST.get('cedula')
        estudiante.correo_institucional = request.POST.get('correo_institucional')
        estudiante.carrera = request.POST.get('carrera')
        estudiante.tipo_practica = request.POST.get('tipo_practica')
        estudiante.semestre = request.POST.get('semestre')
        estudiante.periodo_academico = request.POST.get('periodo_academico')

        estudiante.save()
        messages.success(request, 'Estudiante actualizado correctamente')
        return redirect('lista_estudiantes')

    return redirect('lista_estudiantes')


# ============================
# REMOVER ESTUDIANTE DEL GRUPO
# ============================
@login_required
def remover_estudiante_grupo(request, id):
    docente = get_object_or_404(Docente, user=request.user)
    estudiante = get_object_or_404(Estudiante, id=id, docente=docente)

    if estudiante.grupo:
        estudiante.grupo = None
        estudiante.save()
        messages.success(request, f"{estudiante.nombre} {estudiante.apellido} ha sido removido del grupo")
    else:
        messages.warning(request, f"{estudiante.nombre} {estudiante.apellido} no está asignado a ningún grupo")

    return redirect('lista_estudiantes')


# ============================
# LISTA DE GRUPOS
# ============================
@login_required
def lista_grupos(request):
    docente = get_object_or_404(Docente, user=request.user)
    grupos = Grupo.objects.filter(docente=docente)
    return render(request, 'grupos.html', {'grupos': grupos})


# ============================
# CREAR GRUPO
# ============================
@login_required
def crear_grupo(request):
    return render(request, 'grupo_form.html')


# ============================
# GUARDAR GRUPO
# ============================
@login_required
def guardar_grupo(request):
    if request.method == 'POST':
        docente = get_object_or_404(Docente, user=request.user)
        total = Grupo.objects.filter(docente=docente).count() + 1

        nombre = request.POST.get('nombre').strip() or f"Grupo {total}"

        Grupo.objects.create(
            docente=docente,
            numero=total,
            nombre=nombre,
            actividades_realizadas=request.POST.get('actividades_realizadas'),
            latitud=request.POST.get('latitud') or None,
            longitud=request.POST.get('longitud') or None,
        )

        messages.success(request, f'Grupo "{nombre}" creado correctamente')
        return redirect('lista_grupos')

    return redirect('lista_grupos')


# ============================
# ELIMINAR GRUPO
# ============================
@login_required
def eliminar_grupo(request, id):
    docente = get_object_or_404(Docente, user=request.user)
    grupo = get_object_or_404(Grupo, id=id, docente=docente)

    Estudiante.objects.filter(grupo=grupo).update(grupo=None)

    grupo.delete()
    messages.success(request, f'Grupo {grupo.numero} eliminado correctamente')
    return redirect('lista_grupos')


# ============================
# ASIGNAR ESTUDIANTES A GRUPO
# ============================
@login_required
def asignar_estudiantes(request, grupo_id):
    docente = get_object_or_404(Docente, user=request.user)
    grupo = get_object_or_404(Grupo, id=grupo_id, docente=docente)
    estudiantes = Estudiante.objects.filter(docente=docente)

    if request.method == 'POST':
        ids = request.POST.getlist('estudiantes')

        if len(ids) < 3 or len(ids) > 4:
            messages.error(request, 'Cada grupo debe tener entre 3 y 4 estudiantes')
            return redirect('asignar_estudiantes', grupo_id)

        Estudiante.objects.filter(grupo=grupo).update(grupo=None)
        Estudiante.objects.filter(id__in=ids).update(grupo=grupo)

        messages.success(request, 'Grupo actualizado correctamente')
        return redirect('lista_grupos')

    return render(request, 'asignar_estudiantes.html', {
        'grupo': grupo,
        'estudiantes': estudiantes
    })


# ============================
# DETALLE DE GRUPO
# ============================
@login_required
def detalle_grupo(request, grupo_id):
    docente = get_object_or_404(Docente, user=request.user)
    grupo = get_object_or_404(Grupo, id=grupo_id, docente=docente)

    estudiantes_disponibles = Estudiante.objects.filter(docente=docente, grupo__isnull=True)
    estudiantes_grupo = Estudiante.objects.filter(grupo=grupo)

    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')

        if estudiantes_grupo.count() >= 4:
            messages.error(request, 'El grupo ya tiene 4 estudiantes')
            return redirect('detalle_grupo', grupo_id)

        estudiante = get_object_or_404(Estudiante, id=estudiante_id, docente=docente)
        estudiante.grupo = grupo
        estudiante.save()

        messages.success(request, 'Estudiante agregado al grupo')
        return redirect('detalle_grupo', grupo_id)

    return render(request, 'detalle_grupo.html', {
        'grupo': grupo,
        'estudiantes_disponibles': estudiantes_disponibles,
        'estudiantes_grupo': estudiantes_grupo
    })
from django.http import JsonResponse
def validar_cedula_estudiante_unica(request):
    cedula = request.GET.get('cedula', None)
    estudiante_id = request.GET.get('estudiante_id', None)
    
    # Filtramos por cédula
    existe = Estudiante.objects.filter(cedula=cedula)
    
    # Si estamos editando, excluimos al estudiante actual de la búsqueda
    if estudiante_id:
        existe = existe.exclude(id=estudiante_id)
        
    # Retorna True si está disponible, False si ya existe
    return JsonResponse(not existe.exists(), safe=False)

def validar_correo_estudiante_unico(request):
    correo = request.GET.get('correo', None)
    estudiante_id = request.GET.get('estudiante_id', None)
    
    # Filtramos por correo institucional
    existe = Estudiante.objects.filter(correo_institucional=correo)
    
    if estudiante_id:
        existe = existe.exclude(id=estudiante_id)
        
    return JsonResponse(not existe.exists(), safe=False)