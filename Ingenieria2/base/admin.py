from django.contrib import admin

from .models import Administrador, Paciente_Vacuna, Vacuna, Vacunador, Paciente, Turno, Posta, Subzona

admin.site.register(Vacuna)
admin.site.register(Vacunador)
admin.site.register(Paciente)
admin.site.register(Turno)
admin.site.register(Posta)
admin.site.register(Subzona)
admin.site.register(Administrador)
admin.site.register(Paciente_Vacuna)