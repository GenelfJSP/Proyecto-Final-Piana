from itertools import zip_longest
from django.views.generic import TemplateView
from random import sample
from productos.models import Categoria, Producto, Proveedor


class InicioView(TemplateView):
    template_name = 'inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener categorías, productos y proveedores
        categorias = Categoria.objects.all()
        productos = Producto.objects.all()
        proveedores = Proveedor.objects.all()

        # Seleccionar productos y proveedores aleatorios (por ejemplo, 3 de cada uno)
        productos_random = sample(list(productos), min(3, len(productos)))
        proveedores_random = sample(list(proveedores), min(3, len(proveedores)))
        categorias_random = sample(list(categorias), min(3, len(categorias)))

        # Usar zip_longest para combinar las tres listas
        categorias_productos_proveedores = zip_longest(categorias_random, productos_random, proveedores_random)

        context.update({
            'categorias_productos_proveedores': categorias_productos_proveedores,
        })
        
        return context
    
# Vista para la página "About"
class AboutView(TemplateView):
    template_name = 'about.html'
