from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from ..models import Turno
from datetime import date, datetime, timedelta
from django.db.models import Q

# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def enviar_recordatorios():
    fecha_mañana = date.today() + timedelta(days=1)
    turnos = Turno.objects.filter(Q(fecha=fecha_mañana) & Q(aprobacion=True))
    if(turnos.exists()):
        for turno in turnos:
            turno.user.enviar_mail_recordatorio(turno.fecha, turno.vacuna, False)
        print("Recordatorios enviados")



def start():
    scheduler = BackgroundScheduler()
    #ejecutar tarea todos los dias a las 20:15 pm
    trigger = OrTrigger([CronTrigger(day_of_week='mon,tue,wed,thu,fri,sat,sun', hour=10, minute=37)])
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(enviar_recordatorios, trigger)
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)