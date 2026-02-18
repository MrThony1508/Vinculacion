import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from smtplib import SMTPException
from .models import Docente


# ============================
# GENERAR CONTRASEÑA
# ============================
def generar_password(longitud=10):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))


# ============================
# LISTAR DOCENTES
# ============================
@login_required
def lista_docentes(request):
    docentes = Docente.objects.select_related('user').all()
    return render(request, 'lista_docentes.html', {
        'docentes': docentes
    })


# ============================
# NUEVO DOCENTE (FORMULARIO)
# ============================
@login_required
def nuevo_docente(request):
    return render(request, 'docente_form.html')


# ============================
# GUARDAR DOCENTE
# ============================
@login_required
def guardar_docente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        correo = request.POST.get('correo')
        carrera = request.POST.get('carrera')
        asignacion = request.POST.get('asignacion')

        if not correo:
            messages.error(request, 'Debe ingresar un correo')
            return redirect('nuevo_docente')

        

        # Validar cédula
        if Docente.objects.filter(cedula=cedula).exists():
            messages.error(request, 'La cédula ya está registrada')
            return redirect('nuevo_docente')

        password = generar_password()

        user = User.objects.create_user(
            username=correo,
            email=correo,
            password=password
        )

        grupo_docente, _ = Group.objects.get_or_create(name='DOCENTE')
        user.groups.add(grupo_docente)

        Docente.objects.create(
            user=user,
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            correo_institucional=correo,
            carrera=carrera,
            asignacion=asignacion
        )

        try:
            send_mail(
                'Credenciales de acceso',
                f'Usuario: {correo}\nContraseña: {password}',
                settings.DEFAULT_FROM_EMAIL,
                [correo],
                fail_silently=False
            )
        except SMTPException:
            messages.warning(
                request,
                'El docente se registró, pero no se pudo enviar el correo.'
            )

        messages.success(
            request,
            'Docente registrado correctamente'
        )

        return redirect('lista_docentes')

    return redirect('nuevo_docente')

# ============================
# ELIMINAR DOCENTE
# ============================
@login_required
def eliminar_docente(request, id):
    docente = Docente.objects.get(id=id)
    user = docente.user

    docente.delete()
    user.delete()

    messages.success(request, 'Docente eliminado correctamente')
    return redirect('lista_docentes')


# ============================
# EDITAR DOCENTE (FORMULARIO)
# ============================
@login_required
def editar_docente(request, id):
    docente = Docente.objects.get(id=id)
    return render(request, 'docente_editar.html', {
        'docente': docente
    })


# ============================
# PROCESAR EDICIÓN DOCENTE
# ============================
@login_required
def procesar_edicion_docente(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        docente = Docente.objects.get(id=id)

        docente.nombre = request.POST.get('nombre')
        docente.apellido = request.POST.get('apellido')
        docente.cedula = request.POST.get('cedula')
        docente.carrera = request.POST.get('carrera')
        docente.asignacion = request.POST.get('asignacion')

        # Actualizar usuario asociado
        correo = request.POST.get('correo')
        docente.user.username = correo
        docente.user.email = correo

        docente.user.save()
        docente.save()

        messages.success(request, 'Docente actualizado correctamente')
        return redirect('lista_docentes')

    return redirect('lista_docentes')
from django.http import JsonResponse

def validar_cedula_unica(request):
    cedula = request.GET.get('cedula', None)
    # Excluimos al docente actual si estamos editando (opcional)
    docente_id = request.GET.get('docente_id', None)
    
    existe = Docente.objects.filter(cedula=cedula)
    if docente_id:
        existe = existe.exclude(id=docente_id)
        
    # Si existe, retornamos false (no es válido)
    return JsonResponse(not existe.exists(), safe=False)
from django.contrib.auth.models import User
from django.http import JsonResponse

def validar_correo_unico(request):
    correo = request.GET.get('correo', None)
    # Buscamos si ya existe un usuario con ese username/email
    existe = User.objects.filter(username=correo).exists()
    
    # Retornamos True si el correo está libre, False si ya existe
    return JsonResponse(not existe, safe=False)