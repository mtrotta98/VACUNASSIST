import re
from django.forms import ModelForm

from .models import Paciente, Vacunador, Posta

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

#------Formulario para modelo User------#

class FormularioUsuario(ModelForm):
    first_name = forms.CharField(required=True, label='Nombre')
    last_name = forms.CharField(required=True, label='Apellido')
    username = forms.CharField(required=True, label='Email')
    password = forms.CharField(label='Contraseña', required=True, help_text='Debe contener al menos 6 caracteres.', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label='Repita la contraseña', required=True, widget=forms.PasswordInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name','last_name', 'password', 'password_confirm', 'username')

    #------Funcion para verificacion de datos------#

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if(password != password_confirm):
            raise forms.ValidationError('Las contraseñas no coinciden.')

        if(len(password) < 6):
            raise forms.ValidationError('La contraseña debe contener mas de 6 caracteres.')

        usuario = User.objects.filter(Q(username=cleaned_data.get("username")))
        if(usuario.exists()):
            raise forms.ValidationError('El paciente ya esta cargado en el sistema.')

        return cleaned_data


    def __init__(self, *args, **kwargs):
        super(FormularioUsuario, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

 #------Formulario para modelo Paciente------#

class FormularioPaciente(ModelForm):
    dni = forms.CharField(required=True, label='Dni', help_text='Ingrese el dni sin puntos.')
    fecha_de_nacimiento = forms.DateField(required=True, label='Fecha Nacimiento', widget=forms.DateInput(attrs={'type': 'date', 'max': '2019-12-31', 'min': '1932-01-01'}))

     #------Funcion para verificacion de datos------#

    def clean(self):
        cleaned_data = super().clean()
        dni = cleaned_data.get("dni")

        if('.' in dni):
            raise forms.ValidationError('El dni no debe contener puntos.')

        if((len(dni) < 8) or (int(dni) < 20000000)):
            raise forms.ValidationError('Dni invalido.')

        paciente = Paciente.objects.filter(dni=dni)
        if(paciente.exists()):
            raise forms.ValidationError('El paciente ya esta cargado en el sistema.')

        return cleaned_data

    class Meta():
        model = Paciente
        fields = ["dni", "fecha_de_nacimiento"]
        exclude = ('user', 'token', 'rol', 'posta')

    def __init__(self, *args, **kwargs):
        super(FormularioPaciente, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class FormularioVacunador(ModelForm):
    dni = forms.CharField(required=True, label='Dni', help_text='Ingrese el dni sin puntos.')
    fecha_de_nacimiento = forms.DateField(required=True, label='Fecha Nacimiento', widget=forms.DateInput(attrs={'type': 'date', 'max': '2019-12-31', 'min': '1932-01-01'}))

    def clean(self):
        cleaned_data = super().clean()
        dni = cleaned_data.get("dni")

        if('.' in dni):
            raise forms.ValidationError('El dni no debe contener puntos.')

        if((len(dni) < 8) or (int(dni) < 20000000)):
            raise forms.ValidationError('Dni invalido.')

        vacunador = Vacunador.objects.filter(dni=dni)
        if(vacunador.exists()):
            raise forms.ValidationError('El vacunador ya esta cargado en el sistema.')

        return cleaned_data
    
    class Meta():
        model = Vacunador
        fields = ["dni", "fecha_de_nacimiento"]
        exclude = ('user', 'rol', 'posta')

    def __init__(self, *args, **kwargs):
        super(FormularioVacunador, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

#-------Formulario para modificar modelo User------#

class FormularioModificarUsuario(ModelForm):
    first_name = forms.CharField(required=True, label='Nombre')
    last_name = forms.CharField(required=True, label='Apellido')
    username = forms.CharField(required=True, label='Email')
    #password = forms.CharField(label='Contraseña', required=True, help_text='Debe contener al menos 6 caracteres.', widget=forms.PasswordInput())
    #password_confirm = forms.CharField(label='Repita la contraseña', required=True, widget=forms.PasswordInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('username','first_name','last_name')

    #------Funcion para verificacion de datos------#

    #def clean(self):
        #cleaned_data = super().clean()
        #password = cleaned_data.get("password")
        #password_confirm = cleaned_data.get("password_confirm")

        #if(password != password_confirm):
            #raise forms.ValidationError('Las contraseñas no coinciden.')

        #if(len(password) < 6):
            #raise forms.ValidationError('La contraseña debe contener mas de 6 caracteres.')

        #return cleaned_data


    def __init__(self, *args, **kwargs):
        super(FormularioModificarUsuario, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


#-------Formulario para modificar modelo Paciente------#

class FormularioModificarPaciente(ModelForm):
    dni = forms.CharField(required=True, label='Dni', help_text='Ingrese el dni sin puntos.', widget=forms.TextInput(attrs={'readonly': 'True'}))
    fecha_de_nacimiento = forms.DateField(required=True, label='Fecha Nacimiento', widget=forms.DateInput(attrs={'type': 'date', 'max': '2019-12-31', 'min': '1932-01-01', 'readonly': 'True'}))

     #------Funcion para verificacion de datos------#

    def clean(self):
        cleaned_data = super().clean()
        dni = cleaned_data.get("dni")

        if('.' in dni):
            raise forms.ValidationError('El dni no debe contener puntos.')

        if((len(dni) < 8) or (int(dni) < 20000000)):
            raise forms.ValidationError('Dni invalido.')

        return cleaned_data

    class Meta():
        model = Paciente
        fields = ["dni", "fecha_de_nacimiento"]
        exclude = ('user', 'token', 'rol', 'posta')

    def __init__(self, *args, **kwargs):
        super(FormularioModificarPaciente, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


#-------Formulario para modificar modelo Vacunador------#

class FormularioModificarVacunador(ModelForm):
    dni = forms.CharField(required=True, label='Dni', help_text='Ingrese el dni sin puntos.', widget=forms.TextInput(attrs={'readonly': 'True'}))
    fecha_de_nacimiento = forms.DateField(required=True, label='Fecha Nacimiento', widget=forms.DateInput(attrs={'type': 'date', 'max': '2019-12-31', 'min': '1932-01-01', 'readonly': 'True'}))

     #------Funcion para verificacion de datos------#

    def clean(self):
        cleaned_data = super().clean()
        dni = cleaned_data.get("dni")

        if('.' in dni):
            raise forms.ValidationError('El dni no debe contener puntos.')

        if((len(dni) < 8) or (int(dni) < 20000000)):
            raise forms.ValidationError('Dni invalido.')

        return cleaned_data

    class Meta():
        model = Vacunador
        fields = ["dni", "fecha_de_nacimiento"]
        exclude = ('user', 'token', 'rol', 'posta')

    def __init__(self, *args, **kwargs):
        super(FormularioModificarVacunador, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


#-------Formulario ver Usuario-------#

class FormularioVerUsuario(ModelForm):
    class Meta():
        model = User
        fields = ('first_name','last_name',  'username')
        exclude = ('password','username')

    def __init__(self, *args, **kwargs):
        super(FormularioVerUsuario, self).__init__(*args, **kwargs)
        self.fields["first_name"].disabled = True
        self.fields["last_name"].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

#-------Formulario ver Paciente-------#

class FormularioVerPaciente(ModelForm):
    class Meta():
        model = Paciente
        fields = ["dni", "fecha_de_nacimiento"]
        exclude = ('user', 'token', 'rol','posta')

    def __init__(self, *args, **kwargs):
        super(FormularioVerPaciente, self).__init__(*args, **kwargs)
        self.fields["dni"].disabled = True
        self.fields["fecha_de_nacimiento"].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

#-------Formulario ver Paciente-------#

class FormularioVerVacunador(ModelForm):
    class Meta():
        model = Vacunador
        fields = ["dni", "fecha_de_nacimiento"]
        exclude = ('user', 'token', 'rol','posta')

    def __init__(self, *args, **kwargs):
        super(FormularioVerVacunador, self).__init__(*args, **kwargs)
        self.fields["dni"].disabled = True
        self.fields["fecha_de_nacimiento"].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'




#-------Formulario cambiar contraseña-------#
class FormularioCambioContraseña(ModelForm):
    new_password = forms.CharField(label='Nueva contraseña', required=True, help_text='Debe contener al menos 6 caracteres.', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password_confirm = forms.CharField(label='Repita la contraseña', required=True, widget=forms.PasswordInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('new_password', 'password_confirm')
        exclude = ['username']

    #-------Verificacion de datos-------#

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        password_confirm = cleaned_data.get("password_confirm")

        if(new_password != password_confirm):
            raise forms.ValidationError('Las contraseñas no coinciden.')

        if(len(new_password) < 6):
            raise forms.ValidationError('La contraseña debe contener mas de 6 caracteres.')

        return cleaned_data


    def __init__(self, *args, **kwargs):
        super(FormularioCambioContraseña, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'