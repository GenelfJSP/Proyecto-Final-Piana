from django.urls import path, include
from .views import InicioView, AboutView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from productos.views import ( 
    buscar_productos_por_categoria,
    buscar_productos_por_proveedor,
    buscar_proveedores_por_producto
)

def redirect_inicio(request):
    return redirect('/')

urlpatterns = [
    path('', InicioView.as_view(), name='inicio'),  # Página de inicio
    path('inicio/', redirect_inicio),
    path('about/', AboutView.as_view(), name='about'),  # Página de "about"
    path('usuarios/', include('usuarios.urls')),  # Rutas de usuarios
    path('productos/', include('productos.urls')),  # Rutas de productos
    path('producto_por_categoria/', buscar_productos_por_categoria, name='producto_por_categoria'),
    path('buscar_productos_por_proveedor/', buscar_productos_por_proveedor, name='buscar_productos_por_proveedor'),
    path('buscar_proveedores_por_producto/', buscar_proveedores_por_producto, name='buscar_proveedores_por_producto'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
