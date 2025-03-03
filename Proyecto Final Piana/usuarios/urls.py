from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import (
    UsuariosView,
    ListarUsuariosView, 
    RegistrarUsuarioView, 
    EliminarUsuarioView, 
    RestablecerContrasenaView, 
    IniciarSesionView,
)

urlpatterns = [
    path('iniciar-sesion/', IniciarSesionView.as_view(), name='iniciar_sesion'),  # Iniciar sesión
    path('cerrar-sesion/', LogoutView.as_view(next_page='inicio'), name='cerrar_sesion'),  # Cerrar sesión
    path('registrar_usuario/', RegistrarUsuarioView.as_view(), name='registrar_usuario'),  # Registro
    path('listar_usuarios/', ListarUsuariosView.as_view(), name='listar_usuarios'),  # Listar usuarios
    path('eliminar_usuario/', EliminarUsuarioView.as_view(), name='eliminar_usuario'),  # Eliminar usuario
    path('restablecer-contraseña/', RestablecerContrasenaView.as_view(), name='reestablecimiento_contraseña'),  # Restablecer contraseña
    path('', UsuariosView.as_view(), name='usuarios'),  # Vista principal de usuarios
]
