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
    path('ver_mis_vacunas/', views.verMisVacunas, name='ver_mis_vacunas'),
]