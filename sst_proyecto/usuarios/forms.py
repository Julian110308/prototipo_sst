from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'rol',
            'tipo_documento',
            'numero_documento',
            'telefono',
            'telefono_emergencia',
            'contacto_emergencia',
            'ficha',
            'programa_formacion',
            'password1',
            'password2'
        ]

        widgets = {
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
        }
