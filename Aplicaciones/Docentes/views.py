import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Count, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce
from smtplib import SMTPException

from .models import Docente, Programa
from Aplicaciones.Estudiantes.models import Estudiante

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
    docentes = Docente.objects.select_related('user').all().order_by('-periodo')
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
# GUARDAR DOCENTE (MODIFICADO)
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
        periodo = request.POST.get('periodo')

        if not correo:
            messages.error(request, 'Debe ingresar un correo')
            return redirect('nuevo_docente')

        # VALIDACIÓN: Solo bloquear si existe la misma cédula en el MISMO periodo
        if Docente.objects.filter(cedula=cedula, periodo=periodo).exists():
            messages.error(request, f'El docente con cédula {cedula} ya está registrado en el periodo {periodo}')
            return redirect('nuevo_docente')

        # BUSCAR USUARIO EXISTENTE O CREAR UNO NUEVO
        user = User.objects.filter(username=correo).first()
        nuevo_usuario = False

        if not user:
            password = generar_password()
            user = User.objects.create_user(
                username=correo,
                email=correo,
                password=password
            )
            grupo_docente, _ = Group.objects.get_or_create(name='DOCENTE')
            user.groups.add(grupo_docente)
            nuevo_usuario = True
        else:
            # Si ya existe, nos aseguramos de que tenga los datos actualizados
            user.first_name = nombre
            user.last_name = apellido
            user.save()

        # CREAR REGISTRO DE DOCENTE
        Docente.objects.create(
            user=user,
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            correo_institucional=correo,
            carrera=carrera,
            asignacion=asignacion,
            periodo=periodo
        )

        # Solo enviar correo si es la primera vez que se crea el usuario
        if nuevo_usuario:
            try:
                send_mail(
                    'Credenciales de acceso',
                    f'Hola {nombre}, se te ha registrado en el sistema.\nUsuario: {correo}\nContraseña: {password}',
                    settings.DEFAULT_FROM_EMAIL,
                    [correo],
                    fail_silently=False
                )
            except SMTPException:
                messages.warning(request, 'Docente registrado, pero falló el envío del correo de bienvenida.')
        else:
            messages.info(request, f'Se vinculó el registro al usuario existente de {nombre}.')

        messages.success(request, 'Docente registrado correctamente')
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
    
    # Solo eliminar al usuario si no tiene otros registros en otros periodos
    if not Docente.objects.filter(user=user).exists():
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
        docente.periodo = request.POST.get('periodo')

        # Actualizar usuario asociado
        correo = request.POST.get('correo')
        docente.user.username = correo
        docente.user.email = correo

        docente.user.save()
        docente.save()

        messages.success(request, 'Docente actualizado correctamente')
        return redirect('lista_docentes')

    return redirect('lista_docentes')


# ============================
# VALIDACIONES AJAX
# ============================
def validar_cedula_unica(request):
    cedula = request.GET.get('cedula', None)
    periodo = request.GET.get('periodo', None)
    docente_id = request.GET.get('docente_id', None)
    
    # Ahora validamos cédula + periodo
    existe = Docente.objects.filter(cedula=cedula, periodo=periodo)
    if docente_id:
        existe = existe.exclude(id=docente_id)
        
    return JsonResponse(not existe.exists(), safe=False)


def validar_correo_unico(request):
    # El correo puede repetirse si es el mismo docente en otro periodo
    # por lo tanto, esta validación es opcional según tu lógica
    return JsonResponse(True, safe=False)


# ============================
# GESTIÓN DE PROGRAMAS
# ============================
@login_required
def lista_programas(request):
    conteo_estudiantes = Estudiante.objects.filter(
        proyecto=OuterRef('proyecto')
    ).values('proyecto').annotate(total=Count('id')).values('total')

    programas = Programa.objects.annotate(
        conteo_real=Coalesce(Subquery(conteo_estudiantes), 0, output_field=IntegerField())
    ).order_by('proyecto')

    return render(request, 'lista_programas.html', {
        'programas': programas
    })


@login_required
def nuevo_programa(request):
    return render(request, 'programa_form.html')


@login_required
def guardar_programa(request):
    if request.method == 'POST':
        proyecto = request.POST.get('proyecto')
        coordinador = request.POST.get('coordinador')
        periodo = request.POST.get('periodo')

        Programa.objects.create(
            proyecto=proyecto,
            coordinador=coordinador,
            periodo=periodo,
        )

        messages.success(request, 'Programa registrado correctamente')
        return redirect('lista_programas')

    return redirect('nuevo_programa')


@login_required
def editar_programa(request, id):
    programa = Programa.objects.get(id=id)
    return render(request, 'programa_editar.html', {
        'programa': programa
    })


@login_required
def procesar_edicion_programa(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        programa = Programa.objects.get(id=id)

        programa.proyecto = request.POST.get('proyecto')
        programa.coordinador = request.POST.get('coordinador')
        programa.periodo = request.POST.get('periodo')

        programa.save()
        messages.success(request, 'Programa actualizado correctamente')
        return redirect('lista_programas')

    return redirect('lista_programas')


@login_required
def eliminar_programa(request, id):
    programa = Programa.objects.get(id=id)
    programa.delete()
    messages.success(request, 'Programa eliminado correctamente')
    return redirect('lista_programas')