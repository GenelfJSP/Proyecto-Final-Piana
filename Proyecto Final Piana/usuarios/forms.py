from django import forms
from .models import Usuario

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'contrasena']

class BuscarClienteForm(forms.Form):
    nombre_usuario = forms.CharField(max_length=50, required=False)

class RestablecerContraseñaForm(forms.Form):
    username = forms.CharField(max_length=150, label="Nombre de usuario")
    nueva_contraseña = forms.CharField(widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        nueva_contraseña = cleaned_data.get('nueva_contraseña')
        confirmar_contraseña = cleaned_data.get('confirmar_contraseña')

        return cleaned_data


class EliminarUsuarioForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=150)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class FormularioForm(forms.ModelForm):
    class Meta:
        model = Usuario 
        fields = ['nombre_usuario', 'contrasena']  # Incluye los campos que deseas en el formulario
