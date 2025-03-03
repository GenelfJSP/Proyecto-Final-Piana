from django.contrib import admin
from .models import Producto, Proveedor, Categoria
from django.utils import timezone  # Importar timezone

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_Producto', 'descripcion', 'proveedor', 'categoria', 'fecha_publicacion', 'esta_disponible')
    search_fields = ('nombre_Producto', 'descripcion')
    list_filter = ('proveedor', 'categoria')
    ordering = ('nombre_Producto',)
    actions = ['marcar_como_disponible']

    def marcar_como_disponible(self, request, queryset):
        queryset.update(fecha_publicacion=timezone.now().date())  # Usar timezone
    marcar_como_disponible.short_description = "Marcar productos como disponibles"

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'id')
    search_fields = ('nombre',)
    list_filter = ('categorias',)
    ordering = ('nombre',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'id')
    search_fields = ('nombre',)
    ordering = ('nombre',)