from email import contentmanager
from this import d
from django.shortcuts import redirect, render
from .forms import FormularioPaciente, FormularioUsuario, FormularioVacunador
from django.template import context
from .forms import FormularioAsignarTurno, FormularioModificarVacunador,FormularioPaciente, FormularioUsuario, FormularioModificarUsuario, FormularioModificarPaciente, FormularioCambioContraseña,FormularioVerUsuario,FormularioVerPaciente, FormularioVerVacunador
from base.models import Posta
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.db.models import Q
from .models import Paciente, Paciente_Vacuna, Turno, Vacunador, Vacuna
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.urls import reverse
from urllib.parse import urlencode
from django.utils.crypto import get_random_string
from . import utils
from pathlib import Path
import os

diccionario_vacunas = { 'Gripe' : 'GR',
    'Covid Primera Dosis' : 'CV1',
    'Covid Segunda Dosis' :  'CV2',
    'Fiebre Amarilla' :'FA',
    'No Aplica' : 'NA'}

diccionario_zonas = { 'Municipalidad' : 'Z1',
        'Cementerio': 'Z2',
        'Terminal': 'Z3',
        'No Aplica':'NA' }

#------Login de paciente-------#
def loginPaciente(request):
    if request.method == 'POST':
        username = request.POST.get ('username')
        password = request.POST.get('password')
        token = request.POST.get('token')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if(user.groups.filter(name='paciente')):
                paciente = Paciente.objects.get(user=user)
                if paciente.token == token:
                    login(request, user)
                    if(paciente.historial == False):
                        return redirect('historial_de_vacunas')
                    else:
                        return redirect('home')
                else:
                    messages.error(request, 'Token invalido')
            else:
                return redirect('login_general')
        else:
            messages.error(request, 'Usuario o password invalidos')
    context = {}
    return render(request, 'base/login_paciente.html', context)

#-------Login de Vacunador/Administrador------#
def loginGeneral(request):
    if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')

         user = authenticate(request, username=username, password=password)
 
         if user is not None:
            if(user.groups.filter(name='paciente')):
                return redirect('login_paciente')
            else:
                login(request, user)
                return redirect('home')
         else:
            messages.error(request, 'Usuario o password invalidos')
    context = {}
    return render(request, 'base/login_general.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

#------Registro de paciente------#
def registrarse(request):
    if(request.method == 'POST'):
        formUsuario = FormularioUsuario(request.POST)
        formPaciente = FormularioPaciente(request.POST)
        if(formUsuario.is_valid() and formPaciente.is_valid()):
            formUsuario.cleaned_data.pop('password_confirm')
            usuario = formUsuario.save(commit=False)
            usuario.set_password(formUsuario.cleaned_data['password'])
            usuario.save()
            usuario = User.objects.get(username=formUsuario.cleaned_data['username'])
            usuario.groups.add(2)
            posta = Posta.objects.get(name__icontains=request.POST.get('posta'))
            paciente = formPaciente.save(commit=False)
            paciente.user = usuario
            paciente.posta = posta
            paciente.token = get_random_string(length=4)
            paciente.enviar_mail_registro()
            paciente.save()
            return redirect('login_paciente')
        else:
            context = {'formUsuario': formUsuario, 'formPaciente': formPaciente}
            return render(request, 'base/registro_paciente.html', context)
    formularioUsuario = FormularioUsuario()
    formularioPaciente = FormularioPaciente()
    context = {'formUsuario': formularioUsuario, 'formPaciente': formularioPaciente}
    return render(request, 'base/registro_paciente.html', context)

def home(request):
    context = {}
    if(request.user.is_authenticated):
        usuario = User.objects.get(username=request.user.username)
        if(usuario.groups.filter(name='paciente')):
            perfil = 'paciente'
        elif(usuario.groups.filter(name='administrador')):
            perfil = 'administrador'
        else:
            perfil = 'vacunador'
        context['perfil'] = perfil
    return render(request, 'base/home.html', context)

#------Creacion de paciente por parte del vacunador------#
@login_required(login_url="login_general")
def crearPaciente(request):
    usuario = User.objects.get(username=request.user.username)
    if(usuario.groups.filter(name='paciente')):
        perfil = 'paciente'
    elif(usuario.groups.filter(name='administrador')):
        perfil = 'administrador'
    else:
        perfil = 'vacunador'
    if(request.method == 'POST'):
        formUsuario = FormularioUsuario(request.POST)
        formPaciente = FormularioPaciente(request.POST)
        if(formUsuario.is_valid() and formPaciente.is_valid()):
            formUsuario.cleaned_data.pop('password_confirm')
            usuario, creado = User.objects.get_or_create(
                username=formUsuario.cleaned_data['username'],
                defaults={'first_name': formUsuario.cleaned_data['first_name'], 'last_name': formUsuario.cleaned_data['last_name']})
            if(creado):
                usuario.set_password(formUsuario.cleaned_data['password'])
                usuario.save()
                usuario = User.objects.get(username=formUsuario.cleaned_data['username'])
                usuario.groups.add(2)
                posta = Posta.objects.get(name__icontains=request.POST.get('posta'))
                paciente = formPaciente.save(commit=False)
                paciente.user = usuario
                paciente.posta = posta
                paciente.save()
                paciente.enviar_mail_registro()
            return redirect('home')
        else:
            context = {'formUsuario': formUsuario, 'formPaciente': formPaciente, 'perfil': perfil}
            return render(request, 'base/crear_paciente.html', context)
    formularioUsuario = FormularioUsuario()
    formularioPaciente = FormularioPaciente()
    context = {'formUsuario': formularioUsuario, 'formPaciente': formularioPaciente, 'perfil': perfil}
    return render(request, 'base/crear_paciente.html', context)

@login_required(login_url="login_general")
def crearVacunador(request):
    usuario = User.objects.get(username=request.user.username)
    if(usuario.groups.filter(name='paciente')):
        perfil = 'paciente'
    elif(usuario.groups.filter(name='administrador')):
        perfil = 'administrador'
    else:
        perfil = 'vacunador'
    if(request.method == 'POST'):
        formUsuario = FormularioUsuario(request.POST)
        formVacunador = FormularioVacunador(request.POST)
        if(formUsuario.is_valid() and formVacunador.is_valid()):
            formUsuario.cleaned_data.pop('password_confirm')
            usuario, creado = User.objects.get_or_create(
                username=formUsuario.cleaned_data['username'],
                defaults={'first_name': formUsuario.cleaned_data['first_name'], 'last_name': formUsuario.cleaned_data['last_name']})
            if(creado):
                usuario.set_password(formUsuario.cleaned_data['password'])
                usuario.save()
                usuario = User.objects.get(username=formUsuario.cleaned_data['username'])
                usuario.groups.add(3)
                posta = Posta.objects.get(name__icontains=request.POST.get('posta'))
                vacunador = formVacunador.save(commit=False)
                vacunador.user = usuario
                vacunador.posta = posta
                vacunador.save()
            return redirect('home')
        else:
            context = {'formUsuario': formUsuario, 'formVacunador': formVacunador, 'perfil': perfil}
            return render(request, 'base/crear_vacunador.html', context)
    formularioUsuario = FormularioUsuario()
    formularioVacunador = FormularioVacunador()
    context = {'formUsuario': formularioUsuario, 'formVacunador': formularioVacunador, 'perfil': perfil}
    return render(request, 'base/crear_vacunador.html', context)
    
##------Modificacion del paciente------#
@login_required(login_url="login_paciente")
def modificarPaciente(request, pk):
    user = User.objects.get(id=pk)
    paciente = Paciente.objects.get(user=user) 
    if(user.groups.filter(name='paciente')):
        perfil = 'paciente'
    elif(user.groups.filter(name='administrador')):
        perfil = 'administrador'
    else:
        perfil = 'vacunador'
    if request.method == 'POST':
        formularioUsuario = FormularioModificarUsuario(request.POST, instance=user)
        formularioPaciente = FormularioModificarPaciente(request.POST, instance=paciente)
        if(formularioUsuario.is_valid() and formularioPaciente.is_valid()):
            #formularioUsuario.cleaned_data.pop('password_confirm')
            usuario = formularioUsuario.save(commit=False)
            #usuario.set_password(formularioUsuario.cleaned_data['password'])
            #update_session_auth_hash(request, usuario)
            usuario.save()
            posta = Posta.objects.get(name__icontains=request.POST.get('posta'))
            paci = formularioPaciente.save(commit=False)
            paci.user = user
            paci.posta = posta
            paci.save()
            return redirect('home')
        else:
            context = {'formUsuario': formularioUsuario, 'formPaciente': formularioPaciente, 'perfil': perfil, 'posta':paciente.posta, 'posta_por_defecto' : paciente.posta.printNombre()}
            return render(request, 'base/registro_paciente.html', context)
    formularioUsuario = FormularioModificarUsuario(instance=user)
    formularioPaciente = FormularioModificarPaciente(instance=paciente)
    context = {'formUsuario': formularioUsuario, 'formPaciente': formularioPaciente, 'perfil': perfil, 'posta':paciente.posta, 'posta_por_defecto' : paciente.posta.printNombre()}
    return render(request, 'base/registro_paciente.html', context)


##------Modificacion del paciente------#
@login_required(login_url="login_general")
def modificarVacunador(request, pk):
    user = User.objects.get(id=pk)
    vacunador = Vacunador.objects.get(user=user) 
    if(user.groups.filter(name='vacunador')):
        perfil = 'vacunador'
    elif(user.groups.filter(name='administrador')):
        perfil = 'administrador'
    else:
        perfil = 'paciente'
    if request.method == 'POST':
        formularioUsuario = FormularioModificarUsuario(request.POST, instance=user)
        formularioPaciente = FormularioModificarVacunador(request.POST, instance=vacunador)
        if(formularioUsuario.is_valid() and formularioPaciente.is_valid()):
            #formularioUsuario.cleaned_data.pop('password_confirm')
            usuario = formularioUsuario.save(commit=False)
            #usuario.set_password(formularioUsuario.cleaned_data['password'])
            #update_session_auth_hash(request, usuario)
            usuario.save()
            posta = Posta.objects.get(name__icontains=request.POST.get('posta'))
            paci = formularioPaciente.save(commit=False)
            paci.user = user
            paci.posta = posta
            paci.save()
            return redirect('home')
        else:
            context = {'formUsuario': formularioUsuario, 'formPaciente': formularioPaciente, 'perfil': perfil, 'posta': vacunador.posta, 'posta_por_defecto': vacunador.posta.printNombre()}
            return render(request, 'base/registro_paciente.html', context)
    formularioUsuario = FormularioModificarUsuario(instance=user)
    formularioVacunador = FormularioModificarVacunador(instance=vacunador)
    context = {'formUsuario': formularioUsuario, 'formPaciente': formularioVacunador, 'perfil': perfil, 'posta': vacunador.posta, 'posta_por_defecto': vacunador.posta.printNombre()}
    return render(request, 'base/registro_paciente.html', context)

#-------ver Paciente-------#
@login_required(login_url="login_paciente")
def verPaciente(request):
    pk = request.user.id
    user = User.objects.get(id=pk)
    paciente = Paciente.objects.get(user=user) 
    formUsuario = FormularioVerUsuario(instance=user)
    formPaciente = FormularioVerPaciente(instance=paciente)
    nombre_posta =paciente.posta.printNombre()
    if(user.groups.filter(name='paciente')):
        perfil = 'paciente'
    elif(user.groups.filter(name='administrador')):
        perfil = 'administrador'
    else:
        perfil = 'vacunador'
    if(request.method == 'POST'):
            return redirect('home')
    context = {'formUsuario': formUsuario, 'formPaciente': formPaciente, 'posta' : nombre_posta, 'perfil': perfil}
    if(request.method == 'POST'):
        return redirect('home')
    return render(request, 'base/ver_paciente.html', context)

 #-------ver vacunador-------#   
@login_required(login_url="login_general")
def verVacunador(request):
    pk = request.user.id
    user = User.objects.get(id=pk)
    vacunador = Vacunador.objects.get(user=user) 
    formUsuario = FormularioVerUsuario(instance=user)
    formVacunador = FormularioVerVacunador(instance=vacunador)
    nombre_posta =vacunador.posta.printNombre()
    if(user.groups.filter(name='paciente')):
        perfil = 'paciente'
    elif(user.groups.filter(name='administrador')):
        perfil = 'administrador'
    else:
        perfil = 'vacunador'
    if(request.method == 'POST'):
        return redirect('home')
    context = {'formUsuario': formUsuario, 'formVacunador': formVacunador, 'posta' : nombre_posta, 'perfil': perfil}
    return render(request, 'base/ver_vacunador.html', context)

#-------Cambio de contraseña vacunador/paciente-------#
@login_required(login_url='login_paciente')
def cambioContraseña(request, pk):
    user = User.objects.get(id=pk)
    usuario = User.objects.get(username=request.user.username)
    if(usuario.groups.filter(name='paciente')):
        perfil = 'paciente'
    elif(usuario.groups.filter(name='administrador')):
        perfil = 'administrador'
    else:
        perfil = 'vacunador'
    if(request.method == 'POST'):
        formUsuario = FormularioCambioContraseña(request.POST, instance=user)
        #user = User.objects.get(username=request.user.username)
        if(formUsuario.is_valid()):
            formUsuario.cleaned_data.pop('password_confirm')
            user = formUsuario.save(commit=False)
            user.set_password(formUsuario.cleaned_data['new_password'])
            update_session_auth_hash(request, user)
            user.save()
            return redirect('home')
        else:
            formUsuario = FormularioCambioContraseña(instance=user)
            context = {'formUsuario': formUsuario, 'perfil': perfil}
            return render(request, 'base/cambio_contraseña.html', context)
    formUsuario = FormularioCambioContraseña(instance=user)
    context = {'formUsuario': formUsuario, 'perfil': perfil}
    return render(request, 'base/cambio_contraseña.html', context)

 #-------eliminar vacunador-------#   
@login_required(login_url="login_general")
def eliminarVacunador(request):
    usuario = User.objects.get(username=request.user.username)
    if(usuario.groups.filter(name='paciente')):
        perfil = 'paciente'
    elif(usuario.groups.filter(name='administrador')):
        perfil = 'administrador'
    else:
        perfil = 'vacunador'
    lista = User.objects.filter(groups__name='vacunador')
    if(lista.exists()):
        context = {"lista" : lista, 'perfil': perfil}
        return render(request, 'base/eliminar_vacunador.html', context)
    else:
        messages.error(request, 'No hay vacunadores cargados.')
        context = {'perfil': perfil}
        return redirect('home')

#-------Borrar vacunador de la base-------#
@login_required(login_url="login_general")
def descartarVacunador(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    lista = User.objects.filter(groups__name='vacunador')
    usuario = User.objects.get(username=request.user.username)
    if(usuario.groups.filter(name='paciente')):
        perfil = 'paciente'
    elif(usuario.groups.filter(name='administrador')):
        perfil = 'administrador'
    else:
        perfil = 'vacunador'
    context = {"lista" : lista, 'perfil': perfil}
    return render(request, 'base/eliminar_vacunador.html', context)

#-------Visualizar turnos del dia como vacunador/administrador. Si es vacunador ademas pasa asistencia-------#
@login_required(login_url="login_general")
def verTurnosDelDiaVacunador(request):
    usuario = User.objects.get(id=request.user.id)
    if(usuario.groups.filter(name='paciente')):
        perfil = 'paciente'
    elif(usuario.groups.filter(name='administrador')):
        perfil = 'administrador'
        turnos = Turno.objects.filter(Q(fecha=date.today()) & Q(aprobacion=True) & Q(asistencia=False))
    else:
        perfil = 'vacunador'
        vacunador = Vacunador.objects.get(user=usuario)
        turnos = Turno.objects.filter(Q(fecha=date.today()) & Q(aprobacion=True) & Q(asistencia=False) & Q(posta=vacunador.posta))
    if(request.method == 'POST'):
        asistencias = request.POST.getlist('turno_asistido')
        for pk in asistencias:
            turno = Turno.objects.filter(pk=pk).update(asistencia=True)
            turno = Turno.objects.get(pk=pk)
            observacion = request.POST.get('observacion'+str(turno.user.id))
            observacion_paciente = Paciente.objects.filter(pk=turno.user.id).update(observaciones=observacion)
            paciente_vacuna = Paciente_Vacuna.objects.create(paciente=turno.user, vacuna=turno.vacuna, fecha=turno.fecha)
            paciente_vacuna.save()
            if(turno.vacuna.name == 'CV1'):
                paciente = Paciente.objects.get(pk=turno.user.id)
                paciente.asignarTurnoCovid2()
            elif(turno.vacuna.name == 'GR'):
                paciente = Paciente.objects.get(pk=turno.user.id)
                paciente.asignarTurnoGripe(False)
        return redirect('home')
    if(turnos.exists()):   
        context = {'perfil':perfil, 'turnos': turnos}
        return render(request, 'base/ver_turnos_del_dia.html', context)
    else:
        messages.error(request, 'No hay turnos diarios.')
        context = {'perfil':perfil}
        return redirect('home')


@login_required(login_url="login_general")
def aceptarTurnoFiebreAmarilla(request):
    usuario = User.objects.get(id=request.user.id)
    if(usuario.groups.filter(name='administrador')):
        perfil = 'administrador'
        turnos = Turno.objects.filter(Q(vacuna__name='FA') & Q(asistencia=False) & Q(aprobacion =False) & Q(cancelado=False))
    if(turnos.exists()):   
        context = {'perfil':perfil, 'turnos': turnos}
        return render(request, 'base/aceptar_turno_fa.html', context)
    else:
        messages.error(request, 'No hay turnos de fiebre amarilla para evaluar.')
        context = {'perfil':perfil}
        return redirect('home')

@login_required(login_url="login_general")
def aceptarTurnoFA(request, pk):
    turno = Turno.objects.get(pk=pk)
    turno.aprobacion = True
    paciente = Paciente.objects.get(id=turno.user.id)
    paciente.enviar_mail_recordatorio(turno.fecha, turno.vacuna, True)
    turno.save()
    return redirect('aceptar_turno_fa')

@login_required(login_url="login_general")
def cancelarTurnoFA(request, pk):
    turno = Turno.objects.get(pk=pk)
    turno.cancelado = True
    turno.save()
    return redirect('aceptar_turno_fa')

@login_required(login_url="login_general")
def turnosCancelados(request):
    usuario = User.objects.get(id=request.user.id)
    if(usuario.groups.filter(name='administrador')):
        perfil = 'administrador'
        turnos = Turno.objects.filter(Q(fecha=date.today()) & Q(cancelado=True) & Q(asistencia=False))
    else:
        perfil = 'vacunador'
        vacunador = Vacunador.objects.get(user=usuario)
        turnos = Turno.objects.filter(Q(fecha=date.today()) & Q(cancelado=True) & Q(asistencia=False) & Q(posta=vacunador.posta))
    if(turnos.exists()):   
        context = {'perfil':perfil, 'turnos': turnos}
        return render(request, 'base/turnos_cancelados_del_dia.html', context)
    else:
        messages.error(request, 'No hay turnos cancelados en el dia.')
        return redirect('home')

#-------Carga de historial de vacunas y asignacion de turnos segun rando de edades y fechas-------#
def historialDeVacunas(request):
    if(request.method == 'POST'):
        paciente = Paciente.objects.get(user=request.user)
        gripe = request.POST.get('gripe')
        covid1 = request.POST.get('covid1')
        covid2 = request.POST.get('covid2')
        fiebreAmarilla = request.POST.get('fiebreAmarilla')

        if(gripe == 'True'):
            paciente.cargarVacunaGripe(request.POST.get('fechaGInput'))
        else:
            paciente.asignarTurnoGripe(True)

        if(covid1 == 'True'):
            paciente.cargarVacunaCovid1(request.POST.get('fechaC1Input'))
        else:
            paciente.asignarTurnoCovid1()

        if(covid2 == 'True'):
            paciente.cargarVacunaCovid2(request.POST.get('fechaC2Input'))
        elif(covid2 == 'False' and covid1 == 'True'):
            paciente.asignarTurnoCovid2()

        if(fiebreAmarilla == 'True'):
            paciente.cargarVacunaFiebreAmarilla(request.POST.get('fechaFBinput'))

        paciente.historial = True
        paciente.save()
        return redirect('home')
    context = {'hoy': date.today()}
    return render(request, 'base/historial_de_vacunas.html', context)


#-------ver vacunas paciente-------#
def verVacunasPaciente(request):
    perfil = 'paciente'

    def filtrar_mis_vacunas(paciente_vacuna):
        if (paciente_vacuna.paciente.user.id == request.user.id):
            return True
        return False

    paciente_vacunas = Paciente_Vacuna.objects.all()
    paciente_vacunas = filter(filtrar_mis_vacunas ,paciente_vacunas)
    paciente_vacunas = list(paciente_vacunas)

    context = {'perfil':perfil, 'vacunas': paciente_vacunas}

    if(request.method == 'POST'):
        return redirect('home')

    if(len(paciente_vacunas)>0):   
        context = {'perfil':perfil, 'vacunas': paciente_vacunas}
        return render(request, 'base/ver_vacunas_paciente.html', context)
    else:
        messages.error(request, 'No existen vacunas en el historial.')
        context = {'perfil':perfil}
        return redirect('home')

#-------Ver turnos paciente-------#
def verTurnosPaciente(request):
    perfil = 'paciente'
    def filtrar_mis_turnos(turnos):
        if (turnos.user.user.id == request.user.id):
            return True
        return False

    turnos = Turno.objects.all()
    turnos = filter(filtrar_mis_turnos ,turnos)
    turnos = list(turnos)

    context = {'perfil':perfil, 'turnos': turnos}

    if(request.method == 'POST'):
        return redirect('home')
        
    if(len(turnos)>0):   
        context = {'perfil':perfil, 'turnos': turnos}
        return render(request, 'base/ver_turnos_paciente.html', context)
    else:
        messages.error(request, 'No existen turnos para el paciente.')
        context = {'perfil':perfil}
        return redirect('home')

#-------Ver vacunas administradas del dia-------#
def verVacunasAdministradas(request):
    usuario = User.objects.get(id=request.user.id)
    if(usuario.groups.filter(name='paciente')):
        perfil = 'paciente'
    elif(usuario.groups.filter(name='administrador')):
        perfil = 'administrador'
    else:
        perfil = 'vacunador'

    def filtrar_vacunas(turnos):
        if perfil == 'vacunador':
            posta_vacunador = Vacunador.objects.get(user=usuario).posta
            return turnos.asistencia & (turnos.fecha == date.today()) & (turnos.posta == posta_vacunador)
        else: 
            return turnos.asistencia & (turnos.fecha == date.today())

    turnos = Turno.objects.all()
    turnos = filter(filtrar_vacunas ,turnos)
    turnos = list(turnos)

    context = {'perfil':perfil, 'turnos': turnos}

    if(request.method == 'POST'):
        return redirect('home')
        
    if(len(turnos)>0):   
        context = {'perfil':perfil, 'turnos': turnos}
        return render(request, 'base/ver_vacunas_administradas.html', context)
    else:
        messages.error(request, 'No hubo vacunas administradas durante el día')
        context = {'perfil':perfil}
        return redirect('home')

#-------Asignar turno a paciente como vacunador-------#


@login_required(login_url="login_general")
def preAsignarTurno(request):
    usuario = User.objects.get(id=request.user.id)
    if(usuario.groups.filter(name='paciente')):
        perfil = 'paciente'
    elif(usuario.groups.filter(name='administrador')):
        perfil = 'administrador'
    else:
        perfil = 'vacunador'
    if(request.method == 'POST'):
        dni_paciente= request.POST.get('dni')
        base_url = reverse('asignar_turno')  
        query_string =  urlencode({'dni_paciente': dni_paciente})  
        url = '{}?{}'.format(base_url, query_string) 

        dni_pacientes =   list(Paciente.objects.values('dni'))




        dni_posibles = []
        for each in dni_pacientes:
            dni_posibles.append(int(each['dni']))

        print("------------")
        print(dni_paciente)
        print(dni_posibles)
        print("------------")
        if not (int(dni_paciente) in dni_posibles):
            messages.error(request, 'El DNI no corresponde a un paciente')
            return redirect('pre_asignar_turno')
        else:
            paciente = Paciente.objects.get(dni=int(dni_paciente))
            vacunas_disponibles = ["Covid Primera Dosis", "Covid Segunda Dosis", "Gripe", 'Fiebre Amarilla']
            vacunas_dadas = Paciente_Vacuna.objects.filter(paciente=paciente)
            if paciente.edad() < 18:
                    vacunas_disponibles.remove("Covid Primera Dosis")
                    vacunas_disponibles.remove("Covid Segunda Dosis")
            if paciente.edad() > 60:
                vacunas_disponibles.remove('Fiebre Amarilla')
                
            for vacuna_dada in vacunas_dadas:
                if vacuna_dada.vacuna.name == 'FA' and 'Fiebre Amarilla' in vacunas_disponibles:
                    vacunas_disponibles.remove('Fiebre Amarilla')
                    print('hello2')
                elif vacuna_dada.vacuna.name == 'CV1' and "Covid Primera Dosis" in vacunas_disponibles :
                    vacunas_disponibles.remove('Covid Primera Dosis')
                    print('hello3')
                elif vacuna_dada.vacuna.name == 'CV2'  and "Covid Segunda Dosis" in vacunas_disponibles:
                    vacunas_disponibles.remove('Covid Segunda Dosis')
                elif vacuna_dada.vacuna.name == 'GR' and "Gripe" in vacunas_disponibles and vacuna_dada.fecha.year == date.today().year:
                    vacunas_disponibles.remove('Gripe')  
            if len(vacunas_disponibles) < 1:
                messages.error(request, 'El paciente ya se ha vacunado o no cumple con las condiciones')
                return redirect('pre_asignar_turno')  
            else:
                print('redirect')
                return redirect(url)
    context = {'perfil':perfil}
    return render(request, 'base/pre_asignar_turno.html',context)

@login_required(login_url="login_general")
def asignarTurno(request):
    usuario = User.objects.get(id=request.user.id)
    if(usuario.groups.filter(name='paciente')):
        perfil = 'paciente'
    elif(usuario.groups.filter(name='administrador')):
        perfil = 'administrador'
    else:
        perfil = 'vacunador'
    dni_paciente = request.GET.get('dni_paciente')
    usuario = User.objects.get(id=request.user.id)
    posta_vacunador = Vacunador.objects.get(user=usuario).posta.printNombre()

    paciente = Paciente.objects.get(dni=int(dni_paciente))
    vacunas_disponibles = ["Covid Primera Dosis", "Covid Segunda Dosis", "Gripe", 'Fiebre Amarilla']
    vacunas_dadas = Paciente_Vacuna.objects.filter(paciente=paciente)
    if paciente.edad() < 18:
            vacunas_disponibles.remove("Covid Primera Dosis")
            vacunas_disponibles.remove("Covid Segunda Dosis")
    if paciente.edad() > 60:
        vacunas_disponibles.remove('Fiebre Amarilla')

    for vacuna_dada in vacunas_dadas:
        if vacuna_dada.vacuna.name == 'FA' and 'Fiebre Amarilla' in vacunas_disponibles:
            vacunas_disponibles.remove('Fiebre Amarilla')
        elif vacuna_dada.vacuna.name == 'CV1' and "Covid Primera Dosis" in vacunas_disponibles :
            vacunas_disponibles.remove('Covid Primera Dosis')
        elif vacuna_dada.vacuna.name == 'CV2'  and "Covid Segunda Dosis" in vacunas_disponibles:
            vacunas_disponibles.remove('Covid Segunda Dosis')
        elif vacuna_dada.vacuna.name == 'GR' and "Gripe" in vacunas_disponibles and vacuna_dada.fecha.year == date.today().year:
            vacunas_disponibles.remove('Gripe')     
        
    if(request.method == 'POST'):
        vacuna=request.POST.get("vacunas disponibles")
        vacuna = Vacuna.objects.get(name=diccionario_vacunas[vacuna])
        posta = Posta.objects.get(name=diccionario_zonas[posta_vacunador])
        turno = Turno.objects.create(user=paciente, posta=posta, vacuna=vacuna, fecha=date.today(), aprobacion=True)
        turno.save()

        return redirect('home')

    context = {'hoy': date.today(), 'posta': posta_vacunador, 'vacunas_disponibles': vacunas_disponibles, 'dni_paciente' : dni_paciente, 'nombre_paciente' :paciente,'perfil':perfil  }
    return render(request, 'base/asignar_turno.html', context)



def reservarTurnoFA(request):
    paciente = Paciente.objects.get(user__id=request.user.id)
    perfil = 'paciente'
    turno = Turno.objects.filter((Q(aprobacion=True) | Q(aprobacion=False)) & Q(cancelado=False) & Q(asistencia=False) & Q(vacuna__name='FA') & Q(user=paciente))
    vacuna_dada = Paciente_Vacuna.objects.filter(Q(paciente=paciente) & Q(vacuna__name='FA'))
    if(request.method == 'POST'):      
        vacuna = Vacuna.objects.get(name='FA')
        fecha = request.POST.get('fecha')  
        turno = Turno.objects.create(user=paciente, posta=paciente.posta, vacuna=vacuna, fecha=fecha)
        turno.save()

        return redirect('home')
    if(paciente.calcularEdad() > 60):
        messages.error(request, 'Usted no puede reservar turno por ser mayor de 60 años')
        context = {'perfil':perfil}
        return redirect('home')
    elif(turno.exists()):
        messages.error(request, 'Usted no puede reservar turno por que ya posee un turno')
        context = {'perfil':perfil}
        return redirect('home')
    elif(vacuna_dada.exists()):
        messages.error(request, 'Usted ya se aplico la vacuna de fiebre amarilla')
        context = {'perfil':perfil}
        return redirect('home')
    else:
        context = {'perfil': perfil, 'hoy': date.today()}
        return render(request, 'base/reserva_turno_fa.html', context)

def GenerarComprobante(request, pk):
    vacuna = Paciente_Vacuna.objects.get(pk=pk)
    template_name = "base/comprobante.html"
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join( BASE_DIR , 'static') 
    return utils.render_pdf(
        template_name,
        {
            "vacuna": vacuna,
            "path": path,
        },
    )