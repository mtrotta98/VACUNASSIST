#from time import time
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date, datetime, timedelta
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.db.models import Q
from datetime import time
from random import randint, choice

class Vacuna(models.Model):
    VACUNAS = [
        ('GR', 'Gripe'),
        ('CV1', 'Covid Primera Dosis'),
        ('CV2', 'Covid Segunda Dosis'),
        ('FA', 'Fiebre Amarilla'),
        ('NA', 'No Aplica'),
    ]   
    name = models.CharField(max_length=3, choices=VACUNAS, default='NA')
    #user = models.ForeignKey('Paciente', on_delete=models.CASCADE) 

    def __str__(self):
        return self.name

    def printNombre(self):
        for tupla in self.VACUNAS:
            if self.name == tupla[0]:
                return tupla[1]


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
    observaciones = models.TextField(null=True, default='')
    historial = models.BooleanField(default=False)

    def enviar_mail_registro(self):
        message = 'Bienvenido ' + self.user.first_name + ' ' + self.user.last_name + ' para mayor seguridad, deberas tener el siguiente token cada vez que ingreses al sistema. Token: ' + self.token
        send_mail('Bienvenido a VACUNASSIST', message, settings.EMAIL_HOST_USER, [self.user.username], fail_silently=False)

    def enviar_mail_recordatorio(self, fecha, vacuna, primer):
        if(primer):
            fecha_str = fecha.strftime("%d/%m/%Y")
            message = 'Hola ' + self.user.first_name + ' ' + self.user.last_name + '. Se te ha asignado turno para la vacuna ' + vacuna.printNombre() + ' el dia ' + fecha_str + ' en la posta ' + self.posta.printNombre() + '.'
        else:
            fecha_str = fecha.strftime("%d/%m/%Y")
            message = 'Hola ' + self.user.first_name + ' ' + self.user.last_name + '. Queremos recordarte que tenes un turno para la vacuna de ' + vacuna.printNombre() + ' el dia ' + fecha_str + ' en la posta ' + self.posta.printNombre() + '.'
        send_mail('Recordatorio de Vacuna.', message, settings.EMAIL_HOST_USER, [self.user.username], fail_silently=False)
    
    def calcularEdad(self):
        return date.today().year - self.fecha_de_nacimiento.year

    def crearHorarioAleatorio(self):
        hora = randint(8, 21)
        minutos = choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        horaTurno = time(hora, minutos)
        return horaTurno

    def cargarVacunaGripe(self, fecha):
        vacuna = Vacuna.objects.get(name='GR')
        gripe = Paciente_Vacuna.objects.create(paciente=self, vacuna=vacuna, fecha=fecha)
        gripe.save()
        fecha_anterior = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_gripe = date(fecha_anterior.year, fecha_anterior.month, fecha_anterior.day)
        if((date.today() - fecha_gripe).days >= 365):
            fecha_turno = date.today() + timedelta(days=5)
            vacuna = Vacuna.objects.get(name='GR')
            turno = Turno.objects.create(user=self, fecha=fecha_turno, posta=self.posta, horario=self.crearHorarioAleatorio(), vacuna=vacuna, aprobacion=True, cancelado=False, asistencia=False)
        else:
            dias = 365 - (date.today() - fecha_gripe).days
            fecha_turno = date.today() + timedelta(days=dias)
            vacuna = Vacuna.objects.get(name='GR')
            turno = Turno.objects.create(user=self, fecha=fecha_turno, posta=self.posta, horario=self.crearHorarioAleatorio(), vacuna=vacuna, aprobacion=True, cancelado=False, asistencia=False)
        self.enviar_mail_recordatorio(turno.fecha, turno.vacuna, True)
        turno.save()

    def cargarVacunaCovid1(self, fecha):
        vacuna = Vacuna.objects.get(name='CV1')
        gripe = Paciente_Vacuna.objects.create(paciente=self, vacuna=vacuna, fecha=fecha)
        gripe.save()

    def cargarVacunaCovid2(self, fecha):
        vacuna = Vacuna.objects.get(name='CV2')
        gripe = Paciente_Vacuna.objects.create(paciente=self, vacuna=vacuna, fecha=fecha)
        gripe.save()

    def cargarVacunaFiebreAmarilla(self, fecha):
        vacuna = Vacuna.objects.get(name='FA')
        gripe = Paciente_Vacuna.objects.create(paciente=self, vacuna=vacuna, fecha=fecha)
        gripe.save()

    def asignarTurnoGripe(self, primera):
        if(primera):
            if(self.calcularEdad() < 18):
                fecha = date.today() + timedelta(days=496)
                vacuna = Vacuna.objects.get(name='GR')
                turno = Turno.objects.create(user=self, fecha=fecha, posta=self.posta, horario=self.crearHorarioAleatorio(), vacuna=vacuna, aprobacion=True, cancelado=False, asistencia=False)
            elif(self.calcularEdad() >= 18 and self.calcularEdad() <= 60):
                fecha = date.today() + timedelta(days=186)
                vacuna = Vacuna.objects.get(name='GR')
                turno = Turno.objects.create(user=self, fecha=fecha, posta=self.posta, horario=self.crearHorarioAleatorio(), vacuna=vacuna, aprobacion=True, cancelado=False, asistencia=False)
            elif(self.calcularEdad() > 60):
                fecha = date.today() + timedelta(days=93)
                vacuna = Vacuna.objects.get(name='GR')
                turno = Turno.objects.create(user=self, fecha=fecha, posta=self.posta, horario=self.crearHorarioAleatorio(), vacuna=vacuna, aprobacion=True, cancelado=False, asistencia=False)
            self.enviar_mail_recordatorio(turno.fecha, turno.vacuna, True)
            turno.save()
        else:
            fecha = date.today() + timedelta(days=366)
            vacuna = Vacuna.objects.get(name='GR')
            turno = Turno.objects.create(user=self, fecha=fecha, posta=self.posta, horario=self.crearHorarioAleatorio(), vacuna=vacuna, aprobacion=True, cancelado=False, asistencia=False)
            self.enviar_mail_recordatorio(turno.fecha, turno.vacuna, True)
            turno.save()

    def asignarTurnoCovid1(self):
        if(self.calcularEdad() < 18):
            pass
        elif(self.calcularEdad() >=18 and self.calcularEdad() <= 60):
            fecha = date.today() + timedelta(days=15)
            vacuna = Vacuna.objects.get(name='CV1')
            turno = Turno.objects.create(user=self, fecha=fecha, posta=self.posta, horario=self.crearHorarioAleatorio(), vacuna=vacuna, aprobacion=True, cancelado=False, asistencia=False)
        elif(self.calcularEdad() > 60):
            fecha = date.today() + timedelta(days=6)
            vacuna = Vacuna.objects.get(name='CV1')
            turno = Turno.objects.create(user=self, fecha=fecha, posta=self.posta, horario=self.crearHorarioAleatorio(), vacuna=vacuna, aprobacion=True, cancelado=False, asistencia=False)
        self.enviar_mail_recordatorio(turno.fecha, turno.vacuna, True)
        turno.save()

    def asignarTurnoCovid2(self):
        covid1 = Paciente_Vacuna.objects.get(Q(paciente=self) & Q(vacuna__name='CV1'))
        fecha_covid1 = datetime.strftime(covid1.fecha, '%Y-%m-%d')
        fecha = datetime.strptime(fecha_covid1, "%Y-%m-%d")
        if((datetime.now() - fecha).days > 19):
            fecha_turno = date.today() + timedelta(days=3)
        else:
            fecha_turno = date(fecha.year, fecha.month, fecha.day) + timedelta(days=22)
        vacuna = Vacuna.objects.get(name='CV2')
        turno = Turno.objects.create(user=self, fecha=fecha_turno, posta=self.posta, horario=self.crearHorarioAleatorio(), vacuna=vacuna, aprobacion=True, cancelado=False, asistencia=False)
        self.enviar_mail_recordatorio(turno.fecha, turno.vacuna, True)
        turno.save()

    def devolverIDdeUSER(self):
        return 
    
    def edad(self):
        today = date.today()
        edad = today.year - self.fecha_de_nacimiento.year  - ((today.month, today.day) < (self.fecha_de_nacimiento.month, self.fecha_de_nacimiento.day))
        return edad


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
    fecha = models.DateField(null=True)

    def __str__(self):
        return self.vacuna.name + ', ' + self.paciente.user.first_name + ' ' + self.paciente.user.last_name

    def antesDelRegistro(self):
        usuario = User.objects.get(id=self.paciente.user.id)
        fecha = date(usuario.date_joined.year, usuario.date_joined.month, usuario.date_joined.day)
        return fecha > self.fecha

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
    cancelado = models.BooleanField(default=False)
    asistencia = models.BooleanField(default=False)

    def estado(self):
        if self.asistencia:
            return "Asistido"
        if self.cancelado:
            return "Cancelado"
        if self.fecha < date.today():
            return "Turno Vencido"    
        if self.aprobacion:
            return "Aprobado"
        else:
            return "Pendiente de aprobación"

