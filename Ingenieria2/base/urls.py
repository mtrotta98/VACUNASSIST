from unicodedata import name
from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="home"),
    path('login_paciente/', views.loginPaciente, name="login_paciente"),
    path('login_general/', views.loginGeneral, name="login_general"),
    path('cerrar_sesion/', views.logoutUser, name="cerrar_sesion"),
    path('registrarse/', views.registrarse, name="registro"),
    path('crear_paciente/', views.crearPaciente, name="crear_paciente"),
    path('crear_vacunador/', views.crearVacunador, name="crear_vacunador"),
    path('modificar_paciente/<str:pk>/', views.modificarPaciente, name="modificar_paciente"),
    path('modificar_vacunador/<str:pk>/', views.modificarVacunador, name="modificar_vacunador"),
    path('ver_paciente/', views.verPaciente, name="ver_paciente"),
    path('ver_vacunador/', views.verVacunador, name="ver_vacunador"),
    path('cambiar_contraseña/<str:pk>/', views.cambioContraseña, name="cambiar_contraseña"),
    path('eliminar_vacunador/', views.eliminarVacunador, name="eliminar_vacunador"),
    path('descartar_vacunador/<str:pk>', views.descartarVacunador, name="descartar_vacunador"),
    path('ver_turnos_del_dia/', views.verTurnosDelDiaVacunador, name='ver_turnos_del_dia_vacunador'),
    path('historial_de_vacunas/', views.historialDeVacunas, name='historial_de_vacunas'),
    path('asignar_turno_paciente/', views.asignarTurnoAPaciente, name='asignar_turno_paciente'),
    path('ver_mis_vacunas/', views.verMisVacunas, name='ver_mis_vacunas'),
    path('ver_mis_turnos/', views.verMisTurnos, name='ver_mis_turnos'),
    path('ver_turnos_fiebre_amarilla/', views.verTurnosFiebreAmarilla, name='ver_turnos_fiebre_amarilla'),
    path('evaluar_turnos/<str:pk>/<str:evaluacion>', views.evaluarTurnosFiebreAmarilla, name='evaluar_turno'),
    path('solicitar_turno_fiebre_amarilla/', views.solicitarTurnoFiebreAmarilla, name='solicitar_turno_fiebre_amarilla'),
    path('vacunas_del_dia', views.verVacunasDelDia, name='vacunas_del_dia'),
    path('turnos_cancelados_del_dia', views.verTurnosCanceladosDelDia, name='turnos_cancelados_del_dia'),
]