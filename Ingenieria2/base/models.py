from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date, datetime, timedelta
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

class Vacuna(models.Model):
    VACUNAS = [
        ('GR', 'Gripe'),
        ('CV1', 'Covid Primera Dosis'),
        ('CV2', 'Covid Primera Segunda'),
        ('FA', 'Fiebre Amarilla'),
        ('NA', 'No Aplica'),
    ]   
    name = models.CharField(max_length=3, choices=VACUNAS, default='NA')
    #user = models.ForeignKey('Paciente', on_delete=models.CASCADE) 

    def __str__(self):
        return self.name


class Vacunador(models.Model):
    posta = models.ForeignKey('Posta', on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dni = models.IntegerField(validators=[
            MaxValueValidator(99999999),
            MinValueValidator(1000000)
        ], null=True)
    fecha_de_nacimiento = models.DateField(validators=[MaxValueValidator(limit_value=date.today),MinValueValidator(date(1900, 1, 1))], null=True) 
    rol = models.CharField(max_length=15, null=True, default='vacunador')
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Paciente(models.Model):
    posta = models.ForeignKey('Posta', on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dni = models.IntegerField(validators=[
            MaxValueValidator(99999999),
            MinValueValidator(1000000)
        ], null=True)
    fecha_de_nacimiento = models.DateField(validators=[MaxValueValidator(limit_value=date.today),MinValueValidator(date(1900, 1, 1))], null=True) 
    token = models.CharField(max_length=4,default=get_random_string(length=4),unique=False)
    #vacunas = models.ManyToManyField(Vacuna)
    rol = models.CharField(max_length=15, null=True, default='paciente')

    def enviar_mail_registro(self):
        message = 'Bienvenido ' + self.user.first_name + ' ' + self.user.last_name + ' para mayor seguridad, deberas tener el siguiente token cada vez que ingreses al sistema. Token: ' + self.token
        send_mail('Bienvenido a VACUNASSIST', message, settings.EMAIL_HOST_USER, [self.user.email], fail_silently=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Administrador(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dni = models.IntegerField(validators=[
            MaxValueValidator(99999999),
            MinValueValidator(1000000)
        ], null=True)
    rol = models.CharField(max_length=15, null=True, default='administrador')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Paciente_Vacuna(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, null=True)
    vacuna = models.ForeignKey('Vacuna', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.vacuna.name + ', ' + self.paciente.user.first_name + ' ' + self.paciente.user.last_name

class Subzona(models.Model):
    posta = models.ForeignKey('Posta', on_delete=models.CASCADE)
    name = models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.name

class Posta(models.Model):
    ZONAS = [
        ('Z1', 'Municipalidad'),
        ('Z2', 'Cementerio'),
        ('Z3', 'Terminal'),
        ('NA', 'No Aplica'),
    ]   
    name = models.CharField(max_length=3, choices=ZONAS, default='NA')    

    def printNombre(self):
        for tupla in self.ZONAS:
            if self.name == tupla[0]:
                return tupla[1]

    def __str__(self):
        return self.name

class Turno(models.Model):

    user = models.ForeignKey('Paciente', on_delete=models.CASCADE) 
    fecha = models.DateField(validators=[MinValueValidator(limit_value=date.today),MaxValueValidator(limit_value=(date.today() + timedelta(days=100)))], null=True) 
    posta = models.ForeignKey('Posta', on_delete=models.CASCADE, null=True)
    horario = models.TimeField(null=True)
    vacuna = models.ForeignKey('Vacuna', on_delete=models.CASCADE, null=True)
    aprobacion = models.BooleanField(default=False)
    asistencia = models.BooleanField(default=False)
