from django.http import JsonResponse
from django.views.generic import TemplateView
from random import sample
from productos.models import Categoria, Producto, Proveedor
from itertools import zip_longest
import logging

logger = logging.getLogger(__name__)

class InicioView(TemplateView):
    template_name = 'inicio.html'
    cantidad_a_mostrar = 3  # Número de filas de cards que se muestran al principio
    cards_per_click = 4     # Número de filas de cards que se agregan al hacer clic en "Ver más"
    max_cards = 21          # Límite máximo de filas de cards que se pueden mostrar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener todas las categorías, productos y proveedores
        categorias = list(Categoria.objects.all())
        productos = list(Producto.objects.all())
        proveedores = list(Proveedor.objects.all())

        # Seleccionar elementos aleatorios sin repetir
        categorias_random = sample(categorias, min(self.max_cards, len(categorias))) if categorias else []
        productos_random = sample(productos, min(self.max_cards, len(productos))) if productos else []
        proveedores_random = sample(proveedores, min(self.max_cards, len(proveedores))) if proveedores else []

        # Combinar en una lista de tuplas (categoría, producto, proveedor)
        combined_data = list(zip_longest(categorias_random, productos_random, proveedores_random, fillvalue=None))

        # Pasar los datos al contexto
        context.update({
            'categorias_productos_proveedores': combined_data,  # Lista de tuplas (categoría, producto, proveedor)
            'cantidad_a_mostrar': self.cantidad_a_mostrar,
            'cards_per_click': self.cards_per_click,
            'max_cards': self.max_cards,
        })
        return context

# Vista para la página "About"
class AboutView(TemplateView):
    template_name = 'about.html'
