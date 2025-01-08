from django.contrib import admin
from django.urls import path, include
from compras.views import inicio  # Asegúrate de importar la vista de inicio


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('compras.urls')),  # Incluye las URLs de la app "compras"
    path('', inicio, name='inicio'),  # Ruta para la página de inicio
]
