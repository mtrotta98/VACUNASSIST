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
    path('ver_vacunas_paciente/', views.verVacunasPaciente, name='ver_vacunas_paciente'),
    path('ver_turnos_paciente/', views.verTurnosPaciente, name='ver_turnos_paciente'),
    path('ver_vacunas_administradas/', views.verVacunasAdministradas, name='ver_vacunas_administradas'),
    path('asignar_turno/', views.asignarTurno, name='asignar_turno'),
    path('pre_asignar_turno/', views.preAsignarTurno, name='pre_asignar_turno'),
    path('aceptar_turno_fa/', views.aceptarTurnoFiebreAmarilla, name="aceptar_turno_fa"),
    path('aceptarTurnoFA/<str:pk>/', views.aceptarTurnoFA, name="aceptarTurnoFA"),
    path('cancelarTurnoFA/<str:pk>/', views.cancelarTurnoFA, name="cancelarTurnoFA"),
    path('turnos_cancelados_del_dia', views.turnosCancelados, name="turnos_cancelados_del_dia"),
    path('reserva_turno_fa', views.reservarTurnoFA, name="reserva_turno_fa"),
    path('comprobante_vacuna/<str:pk>/', views.GenerarComprobante, name='comprobante_vacuna'),
    path('ver_analytics/', views.verAnalytics, name='ver_analytics'),
    path('pre_registro/', views.preRegistro, name='pre_registro'),
    path('turnos_aprobados/', views.verTurnosAprobados, name='turnos_aprobados'),
    path('ver_subzonas/', views.verSubZonas, name='ver_subzonas'),
    path('modificar_subzona/<str:pk>/', views.modificarSubZona, name='modificar_subzona'),
    path('nuevaSubZona/<str:pk>/', views.nuevaSubZona, name="nuevaSubZona"),
]