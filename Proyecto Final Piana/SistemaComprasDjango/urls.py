from django.contrib import admin
from django.urls import path, include
from compras.views import InicioView  # Asegúrate de importar la vista de inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('compras.urls')),  # Incluye las URLs de la app "compras"
    path('usuarios/', include('usuarios.urls')),  # Rutas de la app 'usuarios'
    path('productos/', include('productos.urls')),  # Rutas de la app 'productos'
]
