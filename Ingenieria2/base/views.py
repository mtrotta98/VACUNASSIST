from email import contentmanager
from django.shortcuts import redirect, render
from .forms import FormularioPaciente, FormularioUsuario, FormularioVacunador
from django.template import context
from .forms import FormularioModificarVacunador,FormularioPaciente, FormularioUsuario, FormularioModificarUsuario, FormularioModificarPaciente, FormularioCambioContraseña,FormularioVerUsuario,FormularioVerPaciente, FormularioVerVacunador
from base.models import Posta
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.db.models import Q
from .models import Paciente, Vacunador
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

#------Login de paciente-------#
def loginPaciente(request):
    if request.method == 'POST':
        username = request.POST.get ('username')
        password = request.POST.get('password')
        token = request.POST.get('token')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            paciente = Paciente.objects.get(user=user)
            if paciente.token == token:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Token invalido')
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
            paciente.save()
            paciente.enviar_mail_registro()
            login(request, usuario)
            return redirect('home')
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
            context = {'formUsuario': formularioUsuario, 'formPaciente': formularioPaciente, 'perfil': perfil}
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
            context = {'formUsuario': formularioUsuario, 'formVacunador': formularioVacunador, 'perfil': perfil}
            return render(request, 'base/registro_paciente.html', context)
    formularioUsuario = FormularioModificarUsuario(instance=user)
    formularioVacunador = FormularioModificarVacunador(instance=vacunador)
    context = {'formUsuario': formularioUsuario, 'formPaciente': formularioVacunador, 'perfil': perfil}
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
    context = {"lista" : lista, 'perfil': perfil}
    return render(request, 'base/eliminar_vacunador.html', context)

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