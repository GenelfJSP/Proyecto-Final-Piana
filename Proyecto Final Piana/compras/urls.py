from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('usuarios/', views.usuarios, name='usuarios'),
    path('proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('buscar_proveedor/', views.buscar_proveedor, name='buscar_proveedor'),
    path('productos/', views.productos, name='productos'),
    path('restablecer-contraseña/', views.reestablecimiento_contraseña, name='reestablecimiento_contraseña'),
    path('eliminar_usuario/', views.eliminar_usuario, name='eliminar_usuario'),
    path('cerrar-sesion/', LogoutView.as_view(next_page='inicio'), name='cerrar_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('productos/', views.listar_productos, name='listar_productos'),
    path('producto/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('producto/agregar/', views.agregar_producto, name='agregar_producto'),
    path('proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path('proveedor/<int:proveedor_id>/eliminar/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('buscar/proveedor/', views.buscar_proveedor, name='buscar_proveedor'),
    path('buscar/productos_por_proveedor/', views.buscar_productos_por_proveedor, name='buscar_productos_por_proveedor'),
    path('buscar/proveedores_por_producto/', views.buscar_proveedores_por_producto, name='buscar_proveedores_por_producto'),

]
