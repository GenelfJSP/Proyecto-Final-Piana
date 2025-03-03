from django import forms
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import EliminarUsuarioForm, RestablecerContraseñaForm
from django.views.generic import View, TemplateView, ListView
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page

# Vista de usuarios
class UsuariosView(TemplateView):
    template_name = 'usuarios.html'

# Formulario de registro de usuario
class FormularioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

# Vista para registrar usuario
class RegistrarUsuarioView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.error(request, "No puedes crear una cuenta mientras estés logueado.")
            return redirect('usuarios')
        form = FormularioForm()
        return render(request, 'registrar_usuario.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.error(request, "No puedes crear una cuenta mientras estés logueado.")
            return redirect('usuarios')
        form = FormularioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}!')
            return redirect('iniciar_sesion')
        else:
            messages.error(request, 'El nombre de usuario ya está en uso.')
        return render(request, 'registrar_usuario.html', {'form': form})

# Vista para eliminar usuario
class EliminarUsuarioView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.error(request, "No puedes eliminar cuentas mientras estés logueado.")
            return redirect('usuarios')
        form = EliminarUsuarioForm()
        return render(request, 'eliminar_usuario.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.error(request, "No puedes eliminar cuentas mientras estés logueado.")
            return redirect('usuarios')
        form = EliminarUsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    user_to_delete = User.objects.get(username=username)
                    user_to_delete.delete()
                    messages.success(request, f"Usuario {username} eliminado con éxito.")
                    return redirect('listar_usuarios')
                except User.DoesNotExist:
                    messages.error(request, "El usuario no existe.")
            else:
                messages.error(request, "Credenciales incorrectas.")
        else:
            messages.error(request, "Por favor, corrija los errores en el formulario.")
        return render(request, 'eliminar_usuario.html', {'form': form})

# Vista para iniciar sesión
class IniciarSesionView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.error(request, "Ya estás logueado, no puedes iniciar sesión de nuevo.")
            return redirect('usuarios')
        form = AuthenticationForm()
        return render(request, 'iniciar_sesion.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.error(request, "Ya estás logueado, no puedes iniciar sesión de nuevo.")
            return redirect('usuarios')
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Has iniciado sesión correctamente')
                return redirect('usuarios')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Por favor, ingresa los datos correctamente.')
        return render(request, 'iniciar_sesion.html', {'form': form})

# Vista para cerrar sesión
class CerrarSesionView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Sesión cerrada exitosamente.")
        return redirect('inicio')

# Vista para restablecer contraseña
class RestablecerContrasenaView(View):
    def get(self, request):
        form = RestablecerContraseñaForm()
        return render(request, 'reestablecimiento_contraseña.html', {'form': form})

    def post(self, request):
        form = RestablecerContraseñaForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            nueva_contraseña = form.cleaned_data['nueva_contraseña']
            confirmar_contraseña = form.cleaned_data['confirmar_contraseña']

            # Validar que las contraseñas coincidan
            if nueva_contraseña != confirmar_contraseña:
                messages.error(request, "Las contraseñas no coinciden.")
                return render(request, 'reestablecimiento_contraseña.html', {'form': form})

            try:
                user = User.objects.get(username=username)
                user.set_password(nueva_contraseña)
                user.save()
                messages.success(request, f"Contraseña cambiada con éxito. Usuario: {username}.")
                return redirect('iniciar_sesion')
            except User.DoesNotExist:
                messages.error(request, "El nombre de usuario no existe.")
        return render(request, 'reestablecimiento_contraseña.html', {'form': form})

# Vista para listar usuarios
class ListarUsuariosView(View):
    def get(self, request):
        usuarios_list = User.objects.all().order_by('id')

        page_number = int(request.GET.get('page', 1))  # Página actual
        users_per_page = 5  # Usuarios por página normal
        users_per_click = 10  # Usuarios al hacer "Mostrar más"

        # Detectar si es una petición AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            current_page_offset = (page_number - 1) * users_per_page  # Usuarios ya cargados en la paginación normal
            offset = int(request.GET.get('offset', current_page_offset + users_per_page))  # Evitar repetidos con la paginación

            usuarios = list(usuarios_list[offset:offset + users_per_click].values('id', 'username'))
            has_next = offset + users_per_click < usuarios_list.count()

            return JsonResponse({
                'usuarios': usuarios,
                'has_next': has_next,
                'new_offset': offset + users_per_click
            })

        # Paginación normal para la carga inicial
        paginator = Paginator(usuarios_list, users_per_page)
        try:
            usuarios = paginator.page(page_number)
        except PageNotAnInteger:
            usuarios = paginator.page(1)
        except EmptyPage:
            usuarios = paginator.page(paginator.num_pages)

        return render(request, 'listar_usuarios.html', {
            'usuarios': usuarios,
            'offset': (page_number * users_per_page)  # Asegura que "Mostrar más" empiece después de la página actual
        })