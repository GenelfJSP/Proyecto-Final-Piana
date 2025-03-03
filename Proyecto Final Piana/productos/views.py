from itertools import zip_longest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Producto, Proveedor, Categoria
from .forms import ProveedorForm, ProductoForm
from django.views.generic import View
from django.urls import reverse_lazy
from django.db.models import Count
from random import sample
from django.urls import reverse
from django.template.context_processors import csrf
from django.utils import timezone  # Importar timezone para manejo de fechas
import logging

logger = logging.getLogger(__name__)

# Vista de productos
class ProductosView(TemplateView):
    template_name = 'productos.html'
    cantidad_a_mostrar = 2  # Número de filas de cards que se muestran al principio
    cards_per_click = 3     # Número de filas de cards que se agregan al hacer clic en "Ver más"
    max_cards = 11          # Límite máximo de filas de cards que se pueden mostrar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            # Obtener todas las categorías, productos y proveedores
            categorias = list(Categoria.objects.all())
            productos = list(Producto.objects.all())
            proveedores = list(Proveedor.objects.all())

            # Seleccionar elementos aleatorios sin repetir
            categorias_random = sample(categorias, min(self.max_cards, len(categorias))) if categorias else []
            productos_random = sample(productos, min(self.max_cards, len(productos))) if productos else []
            proveedores_random = sample(proveedores, min(self.max_cards, len(proveedores))) if proveedores else []

            # Combinar en una lista de tuplas (categoría, producto, proveedor)
            categorias_productos_proveedores = list(zip_longest(categorias_random, productos_random, proveedores_random, fillvalue=None))

            # Pasar los datos al contexto
            context.update({
                'categorias_productos_proveedores': categorias_productos_proveedores,
                'cantidad_a_mostrar': self.cantidad_a_mostrar,
                'cards_per_click': self.cards_per_click,
                'max_cards': self.max_cards,
            })
        except Exception as e:
            logger.error(f"Error en ProductosView: {str(e)}")  # Registrar errores
            context.update({
                'categorias_productos_proveedores': [],
                'cantidad_a_mostrar': 0,
                'cards_per_click': 0,
                'max_cards': 0,
            })

        return context

# Vista para listar proveedores
class ListarProveedoresView(View):
    def get(self, request):
        proveedores_list = Proveedor.objects.all().order_by('id')
        page_number = int(request.GET.get('page', 1))
        proveedores_por_pagina = 4    # Cantidad de proveedores en la paginación clásica
        proveedores_por_click = 6    # Cantidad de proveedores que se cargarán al hacer "Mostrar más"

        # Si es una petición AJAX, devolvemos JSON con los siguientes proveedores
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            current_page_offset = (page_number - 1) * proveedores_por_pagina
            offset = int(request.GET.get('offset', current_page_offset + proveedores_por_pagina))
            
            proveedores = proveedores_list[offset:offset + proveedores_por_click]

            # Serializar proveedores incluyendo sus categorías
            proveedores_data = []
            for proveedor in proveedores:
                categorias = list(proveedor.categorias.values_list('nombre', flat=True))  # Extrae solo los nombres
                proveedores_data.append({
                    'id': proveedor.id,
                    'nombre': proveedor.nombre,
                    'descripcion': proveedor.descripcion,
                    'fecha_creacion': proveedor.fecha_creacion.strftime("%d/%m/%Y"),  # Formatear fecha
                    'logotipo': proveedor.logotipo.url if proveedor.logotipo else None,
                    'categorias': ', '.join(categorias) if categorias else "No tiene categorías asignadas."
                })

            has_next = offset + proveedores_por_click < proveedores_list.count()
            return JsonResponse({
                'proveedores': proveedores_data,
                'has_next': has_next,
                'new_offset': offset + proveedores_por_click,
            })

        # Para la carga inicial, utilizamos la paginación clásica
        paginator = Paginator(proveedores_list, proveedores_por_pagina)
        try:
            proveedores = paginator.page(page_number)
        except PageNotAnInteger:
            proveedores = paginator.page(1)
        except EmptyPage:
            proveedores = paginator.page(paginator.num_pages)

        return render(request, 'listar_proveedores.html', {
            'proveedores': proveedores,
            # Este offset asegura que el botón "Mostrar más" comience después de la página actual
            'offset': (page_number * proveedores_por_pagina)
        })

# Iniciar sesion cuando se requiera
class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, "Debe iniciar sesión para realizar esta acción.")
        return redirect('iniciar_sesion')  # Redirige a la página de login

# Vista para agregar o quitar categorias
class AgregarQuitarCategoriaProveedorView(CustomLoginRequiredMixin, View):

    def get(self, request, proveedor_id):
        proveedor = Proveedor.objects.get(id=proveedor_id)
        categorias = Categoria.objects.all()

        # Definir la cantidad de categorías a mostrar por página y por clic
        categorias_por_pagina = 3
        categorias_por_click = 5

        # Paginación para "Categorías que posee"
        categorias_posee = proveedor.categorias.all().order_by('id')
        page_number_posee = int(request.GET.get('page_posee', 1))
        paginator_posee = Paginator(categorias_posee, categorias_por_pagina)
        try:
            categorias_posee_paginated = paginator_posee.page(page_number_posee)
        except PageNotAnInteger:
            categorias_posee_paginated = paginator_posee.page(1)
        except EmptyPage:
            categorias_posee_paginated = paginator_posee.page(paginator_posee.num_pages)

        # Paginación para "Demás Categorías"
        otras_categorias = categorias.filter(proveedores__isnull=True).order_by('id')
        page_number_otras = int(request.GET.get('page_otras', 1))
        paginator_otras = Paginator(otras_categorias, categorias_por_pagina)
        try:
            otras_categorias_paginated = paginator_otras.page(page_number_otras)
        except PageNotAnInteger:
            otras_categorias_paginated = paginator_otras.page(1)
        except EmptyPage:
            otras_categorias_paginated = paginator_otras.page(paginator_otras.num_pages)

        # Detectar si es una petición AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            tipo = request.GET.get('tipo')
            offset = int(request.GET.get('offset', 0))

            if tipo == 'posee':
                categorias_list = list(categorias_posee[offset:offset + categorias_por_click].values('id', 'nombre'))
                has_next = offset + categorias_por_click < categorias_posee.count()
            elif tipo == 'otras':
                categorias_list = list(otras_categorias[offset:offset + categorias_por_click].values('id', 'nombre'))
                has_next = offset + categorias_por_click < otras_categorias.count()
            else:
                categorias_list = []
                has_next = False

            return JsonResponse({
                'categorias': categorias_list,
                'has_next': has_next,
                'new_offset': offset + categorias_por_click
            })

        return render(request, 'agregar_categoria_proveedor.html', {
            'proveedor': proveedor,
            'categorias_posee': categorias_posee_paginated,
            'otras_categorias': otras_categorias_paginated,
            'offset_posee': (page_number_posee * categorias_por_pagina),
            'offset_otras': (page_number_otras * categorias_por_pagina),
            'categorias_por_click': categorias_por_click,
            'eliminar_categoria_url': reverse('eliminar_categoria', args=[proveedor.id, 0]),
            'agregar_categoria_url': reverse('agregar_categoria_proveedor', args=[proveedor.id]),
            'csrf_token': csrf(request)['csrf_token'],
        })
    
    def post(self, request, proveedor_id):
        proveedor = Proveedor.objects.get(id=proveedor_id)
        nueva_categoria = request.POST.get('nueva_categoria')
        categoria_a_quitar_id = request.POST.get('categoria_a_quitar')
        categoria_a_eliminar_id = request.POST.get('categoria_a_eliminar')

        # Agregar nueva categoría
        if nueva_categoria:
            categoria, created = Categoria.objects.get_or_create(nombre=nueva_categoria)
            proveedor.categorias.add(categoria)
            if created:
                messages.success(request, f'Categoría "{nueva_categoria}" agregada a {proveedor.nombre}.')
            else:
                messages.warning(request, f'La categoría "{nueva_categoria}" ya existía y se agregó a {proveedor.nombre}.')

        # Quitar categoría
        if categoria_a_quitar_id:
            categoria_a_quitar = Categoria.objects.get(id=categoria_a_quitar_id)
            proveedor.categorias.remove(categoria_a_quitar)
            messages.success(request, f'Categoría "{categoria_a_quitar.nombre}" eliminada de {proveedor.nombre}.')

        # Eliminar categoría si no tiene proveedores
        if categoria_a_eliminar_id:
            categoria_a_eliminar = Categoria.objects.get(id=categoria_a_eliminar_id)
            if categoria_a_eliminar.proveedores.count() == 0:
                categoria_a_eliminar.delete()
                messages.success(request, f'Categoría "{categoria_a_eliminar.nombre}" eliminada completamente.')
            else:
                messages.warning(request, f'No se puede eliminar la categoría "{categoria_a_eliminar.nombre}" porque está asociada a otros proveedores.')

        return redirect('agregar_categoria_proveedor', proveedor_id=proveedor.id)

# Eliminar categorias
class EliminarCategoriasView(CustomLoginRequiredMixin, View):
    def post(self, request, proveedor_id, categoria_id):
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        categoria = get_object_or_404(Categoria, id=categoria_id)

        # Primero, eliminamos la categoría del proveedor
        if categoria in proveedor.categorias.all():
            proveedor.categorias.remove(categoria)
            messages.success(request, f'La categoría "{categoria.nombre}" ha sido eliminada del proveedor "{proveedor.nombre}".')

        # Verificar si la categoría está asociada a algún producto
        productos_a_eliminar = Producto.objects.filter(categoria=categoria)
        
        if productos_a_eliminar.exists():
            # Si la categoría está asociada a productos, mostramos un mensaje de advertencia
            if productos_a_eliminar.count() == 1:
                messages.warning(request, f'La categoría "{categoria.nombre}" no puede ser eliminada porque está asociada a un producto. Primero debe eliminar el producto.')
            else:
                messages.warning(request, f'No se puede eliminar la categoría "{categoria.nombre}" porque está asociada a productos. Primero debe eliminar los productos.')
        else:
            # Si no hay productos asociados, verificamos si la categoría está asociada a algún otro proveedor
            if categoria.proveedores.count() == 0:
                categoria.delete()  # Eliminamos la categoría
                messages.success(request, f'La categoría "{categoria.nombre}" ha sido eliminada completamente.')
            else:
                messages.warning(request, f'La categoría "{categoria.nombre}" sigue asociada a otros proveedores y no puede ser eliminada.')

        return redirect('agregar_categoria_proveedor', proveedor_id=proveedor.id)

# Vista para eliminar proveedor
class EliminarProveedorView(CustomLoginRequiredMixin, View):
    def get(self, request, proveedor_id):
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        if Producto.objects.filter(proveedor=proveedor).exists():
            messages.error(request, "Este proveedor no se puede eliminar porque tiene productos asociados.")
            return redirect('listar_proveedores')
        proveedor.delete()
        messages.success(request, "Proveedor eliminado exitosamente.")
        return redirect('listar_proveedores')

# Vista para agregar un proveedor
class AgregarProveedorView(CustomLoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'agregar_proveedor.html'
    success_url = reverse_lazy('listar_proveedores')

    def form_valid(self, form):
        # Guardamos el proveedor sin comprometerlo en la base de datos aún
        proveedor = form.save(commit=False)
        proveedor.save()  # Guardamos el proveedor

        # Obtenemos la categoría procesada en el formulario (ya sea la seleccionada o la creada)
        categoria = form.cleaned_data.get('categoria')
        
        # Asociamos la categoría al proveedor si existe
        if categoria:
            proveedor.categorias.add(categoria)

        return super().form_valid(form)

# Vista para listar productos
class ListarProductosView(View):
    def get(self, request):
        productos_list = Producto.objects.all().order_by('id')
        page_number = int(request.GET.get('page', 1))  # Página actual
        productos_por_pagina = 4      # Cantidad de productos por página (paginación clásica)
        productos_por_click = 6      # Cantidad de productos que se cargarán al hacer "Mostrar más"

        # Si la petición es AJAX, se envían los productos en formato JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Se calcula el offset inicial a partir de la paginación clásica
            current_page_offset = (page_number - 1) * productos_por_pagina
            # Se toma el offset que viene en la petición AJAX o se inicia después de la página actual
            offset = int(request.GET.get('offset', current_page_offset + productos_por_pagina))
            productos = list(
                productos_list[offset:offset + productos_por_click].values(
                    'id',
                    'nombre_Producto',
                    'descripcion',
                    'categoria__nombre',
                    'proveedor__nombre',
                    'fecha_publicacion',
                    'foto'  # Asegúrate de que este campo devuelva la URL o ajusta en el template
                )
            )
            has_next = offset + productos_por_click < productos_list.count()

            return JsonResponse({
                'productos': productos,
                'has_next': has_next,
                'new_offset': offset + productos_por_click
            })

        # Paginación clásica para la carga inicial
        paginator = Paginator(productos_list, productos_por_pagina)
        try:
            productos = paginator.page(page_number)
        except PageNotAnInteger:
            productos = paginator.page(1)
        except EmptyPage:
            productos = paginator.page(paginator.num_pages)

        return render(request, 'listar_productos.html', {
            'productos': productos,
            # Se pasa el offset inicial para que "Mostrar más" inicie después de la página actual
            'offset': (page_number * productos_por_pagina)
        })

# Agregar un producto
class AgregarProductoView(CustomLoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'agregar_producto.html'
    success_url = reverse_lazy('listar_productos')  # Redirige a la lista de productos tras crear uno
    def form_valid(self, form):
        producto = form.save(commit=False)  # Guarda el producto sin comprometerlo en la BD
        producto.save()  # Guarda el producto con la imagen incluida
        return super().form_valid(form)

# Vista para eliminar producto
class EliminarProductoView(CustomLoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'eliminar_producto.html'
    success_url = reverse_lazy('listar_productos')

# Buscar Producto por proveedor
def buscar_productos_por_proveedor(request):
    proveedores = Proveedor.objects.all()  # Obtener todos los proveedores
    productos = Producto.objects.none()  # Inicializamos productos como un QuerySet vacío
    proveedor_seleccionado = None
    mensaje = None

    # Intentamos obtener el valor de 'q' en la URL (cuando llegas desde una card)
    proveedor_nombre = request.GET.get('q')

    if proveedor_nombre:  # Si hay un 'q' en la URL, usamos ese valor para hacer la búsqueda
        try:
            proveedor_seleccionado = Proveedor.objects.get(nombre=proveedor_nombre)
            productos = Producto.objects.filter(proveedor=proveedor_seleccionado)
            if not productos.exists():
                mensaje = "Este proveedor no tiene productos disponibles."
        except Proveedor.DoesNotExist:
            mensaje = "Proveedor no encontrado."
    elif request.method == 'POST':  # Si no hay 'q' en la URL, se maneja el formulario POST
        proveedor_id = request.POST.get('proveedor')
        if proveedor_id:  # Si se ha seleccionado un proveedor
            try:
                proveedor_seleccionado = Proveedor.objects.get(id=proveedor_id)
                productos = Producto.objects.filter(proveedor=proveedor_seleccionado)
                if not productos.exists():
                    mensaje = "Este proveedor no tiene productos disponibles."
            except Proveedor.DoesNotExist:
                mensaje = "Proveedor no encontrado."
        else:
            mensaje = "No se seleccionó un proveedor desde el formulario."

    # Paginación clásica
    page_number = int(request.GET.get('page', 1))  # Página actual
    productos_por_pagina = 4  # Cantidad de productos por página (paginación clásica)
    productos_por_click = 6  # Cantidad de productos que se cargarán al hacer "Mostrar más"

    # Si la petición es AJAX, se envían los productos en formato JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Se calcula el offset inicial a partir de la paginación clásica
        current_page_offset = (page_number - 1) * productos_por_pagina
        # Se toma el offset que viene en la petición AJAX o se inicia después de la página actual
        offset = int(request.GET.get('offset', current_page_offset + productos_por_pagina))
        productos_list = productos[offset:offset + productos_por_click].values(
            'id',
            'nombre_Producto',
            'descripcion',
            'categoria__nombre',
            'proveedor__nombre',
            'fecha_publicacion',
            'foto'  # Asegúrate de que este campo devuelva la URL o ajusta en el template
        )
        has_next = offset + productos_por_click < productos.count()

        return JsonResponse({
            'productos': list(productos_list),  # Convertimos el QuerySet a lista para JSON
            'has_next': has_next,
            'new_offset': offset + productos_por_click
        })

    # Paginación clásica para la carga inicial
    paginator = Paginator(productos, productos_por_pagina)
    try:
        productos_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        productos_paginados = paginator.page(1)
    except EmptyPage:
        productos_paginados = paginator.page(paginator.num_pages)

    return render(request, 'buscar_productos_por_proveedor.html', {
        'proveedores': proveedores,
        'productos': productos_paginados,
        'proveedor_seleccionado': proveedor_seleccionado,
        'mensaje': mensaje,
        'offset': (page_number * productos_por_pagina)  # Se pasa el offset inicial
    })

# Buscar proveedor por productos
def buscar_proveedores_por_producto(request):
    productos = Producto.objects.values('nombre_Producto').distinct()  # Obtener todos los productos sin duplicados
    proveedores = Proveedor.objects.none()  # Inicializamos proveedores como un QuerySet vacío
    producto_seleccionado = None
    mensaje = None

    # Intentamos obtener el valor de 'q' en la URL (cuando llegas desde una card)
    producto_nombre = request.GET.get('q')

    if producto_nombre:  # Si hay un 'q' en la URL, usamos ese valor para hacer la búsqueda
        productos_seleccionados = Producto.objects.filter(nombre_Producto=producto_nombre)
        if productos_seleccionados.exists():
            proveedores = Proveedor.objects.filter(producto__in=productos_seleccionados).distinct()
            if not proveedores.exists():
                mensaje = "No se encontraron proveedores para este producto."
            producto_seleccionado = producto_nombre
        else:
            mensaje = "Producto no encontrado."
    elif request.method == 'POST':  # Si no hay 'q' en la URL, se maneja el formulario POST
        producto_nombre = request.POST.get('producto')  # Cambiado para recibir el nombre del producto
        if producto_nombre:  # Si se ha seleccionado un producto
            productos_seleccionados = Producto.objects.filter(nombre_Producto=producto_nombre)  # Usar filter en lugar de get
            if productos_seleccionados.exists():
                proveedores = Proveedor.objects.filter(producto__in=productos_seleccionados).distinct()
                if not proveedores.exists():
                    mensaje = "No se encontraron proveedores para este producto."
                producto_seleccionado = producto_nombre
            else:
                mensaje = "Producto no encontrado."
        else:
            mensaje = "No se seleccionó un producto desde el formulario."

    # Paginación clásica
    page_number = int(request.GET.get('page', 1))  # Página actual
    proveedores_por_pagina = 4  # Cantidad de proveedores por página (paginación clásica)
    proveedores_por_click = 6  # Cantidad de proveedores que se cargarán al hacer "Mostrar más"

    # Si la petición es AJAX, se envían los proveedores en formato JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Se calcula el offset inicial a partir de la paginación clásica
        current_page_offset = (page_number - 1) * proveedores_por_pagina
        # Se toma el offset que viene en la petición AJAX o se inicia después de la página actual
        offset = int(request.GET.get('offset', current_page_offset + proveedores_por_pagina))
        proveedores_list = proveedores[offset:offset + proveedores_por_click].values(
            'id',
            'nombre',
            'descripcion',
            'logotipo'  # Asegúrate de que este campo devuelva la URL o ajusta en el template
        )
        has_next = offset + proveedores_por_click < proveedores.count()

        return JsonResponse({
            'proveedores': list(proveedores_list),  # Convertimos el QuerySet a lista para JSON
            'has_next': has_next,
            'new_offset': offset + proveedores_por_click
        })

    # Paginación clásica para la carga inicial
    paginator = Paginator(proveedores, proveedores_por_pagina)
    try:
        proveedores_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        proveedores_paginados = paginator.page(1)
    except EmptyPage:
        proveedores_paginados = paginator.page(paginator.num_pages)

    return render(request, 'buscar_proveedores_por_producto.html', {
        'productos': productos,
        'proveedores': proveedores_paginados,
        'producto_seleccionado': producto_seleccionado,
        'mensaje': mensaje,
        'offset': (page_number * proveedores_por_pagina)  # Se pasa el offset inicial
    })

# Buscar productos por categoria
def buscar_productos_por_categoria(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    productos = Producto.objects.none()  # Inicializamos productos como un QuerySet vacío
    categoria_seleccionada = None
    mensaje = None

    # Intentamos obtener el valor de 'q' en la URL (cuando llegas desde una card)
    categoria_nombre = request.GET.get('q')

    if categoria_nombre:  # Si hay un 'q' en la URL, usamos ese valor para hacer la búsqueda
        try:
            categoria_seleccionada = Categoria.objects.get(nombre=categoria_nombre)
            productos = Producto.objects.filter(categoria=categoria_seleccionada)
            if not productos.exists():
                mensaje = "No hay productos disponibles para esta categoría."
        except Categoria.DoesNotExist:
            mensaje = "Categoría no encontrada."
    elif request.method == 'POST':  # Si no hay 'q' en la URL, se maneja el formulario POST
        categoria_nombre = request.POST.get('categoria')
        if categoria_nombre:  # Si se ha seleccionado una categoría
            try:
                categoria_seleccionada = Categoria.objects.get(nombre=categoria_nombre)
                productos = Producto.objects.filter(categoria=categoria_seleccionada)
                if not productos.exists():
                    mensaje = "No hay productos disponibles para esta categoría."
            except Categoria.DoesNotExist:
                mensaje = "Categoría no encontrada."
        else:
            mensaje = "No se seleccionó una categoría desde el formulario."

    # Paginación clásica
    page_number = int(request.GET.get('page', 1))  # Página actual
    productos_por_pagina = 4  # Cantidad de productos por página (paginación clásica)
    productos_por_click = 6  # Cantidad de productos que se cargarán al hacer "Mostrar más"

    # Si la petición es AJAX, se envían los productos en formato JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Se calcula el offset inicial a partir de la paginación clásica
        current_page_offset = (page_number - 1) * productos_por_pagina
        # Se toma el offset que viene en la petición AJAX o se inicia después de la página actual
        offset = int(request.GET.get('offset', current_page_offset + productos_por_pagina))
        productos_list = productos[offset:offset + productos_por_click].values(
            'id',
            'nombre_Producto',
            'descripcion',
            'categoria__nombre',
            'proveedor__nombre',
            'fecha_publicacion',
            'foto'  # Asegúrate de que este campo devuelva la URL o ajusta en el template
        )
        has_next = offset + productos_por_click < productos.count()

        return JsonResponse({
            'productos': list(productos_list),  # Convertimos el QuerySet a lista para JSON
            'has_next': has_next,
            'new_offset': offset + productos_por_click
        })

    # Paginación clásica para la carga inicial
    paginator = Paginator(productos, productos_por_pagina)
    try:
        productos_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        productos_paginados = paginator.page(1)
    except EmptyPage:
        productos_paginados = paginator.page(paginator.num_pages)

    return render(request, 'buscar_productos_por_categoria.html', {
        'categorias': categorias,
        'productos': productos_paginados,
        'categoria_seleccionada': categoria_seleccionada,
        'mensaje': mensaje,
        'offset': (page_number * productos_por_pagina)  # Se pasa el offset inicial
    })

# Buscar proveedor por categoria
def buscar_proveedores_por_categoria(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    proveedores = Proveedor.objects.none()  # Inicializamos proveedores como un QuerySet vacío
    categoria_seleccionada = None
    mensaje = None

    # Intentamos obtener el valor de 'q' en la URL (cuando llegas desde una card)
    categoria_nombre = request.GET.get('q')

    if categoria_nombre:  # Si hay un 'q' en la URL, usamos ese valor para hacer la búsqueda
        try:
            categoria_seleccionada = Categoria.objects.get(nombre=categoria_nombre)
            proveedores = Proveedor.objects.filter(categorias=categoria_seleccionada).distinct()
            if not proveedores.exists():
                mensaje = "No hay proveedores disponibles para esta categoría."
        except Categoria.DoesNotExist:
            mensaje = "Categoría no encontrada."
    elif request.method == 'POST':  # Si no hay 'q' en la URL, se maneja el formulario POST
        categoria_nombre = request.POST.get('categoria')
        if categoria_nombre:  # Si se ha seleccionado una categoría
            try:
                categoria_seleccionada = Categoria.objects.get(nombre=categoria_nombre)
                proveedores = Proveedor.objects.filter(categorias=categoria_seleccionada).distinct()
                if not proveedores.exists():
                    mensaje = "No hay proveedores disponibles para esta categoría."
            except Categoria.DoesNotExist:
                mensaje = "Categoría no encontrada."
        else:
            mensaje = "No se seleccionó una categoría desde el formulario."

    # Paginación clásica
    page_number = int(request.GET.get('page', 1))  # Página actual
    proveedores_por_pagina = 4  # Cantidad de proveedores por página (paginación clásica)
    proveedores_por_click = 6  # Cantidad de proveedores que se cargarán al hacer "Mostrar más"

    # Si la petición es AJAX, se envían los proveedores en formato JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Se calcula el offset inicial a partir de la paginación clásica
        current_page_offset = (page_number - 1) * proveedores_por_pagina
        # Se toma el offset que viene en la petición AJAX o se inicia después de la página actual
        offset = int(request.GET.get('offset', current_page_offset + proveedores_por_pagina))
        proveedores_list = proveedores[offset:offset + proveedores_por_click].values(
            'id',
            'nombre',
            'descripcion',
            'logotipo'  # Asegúrate de que este campo devuelva la URL o ajusta en el template
        )
        has_next = offset + proveedores_por_click < proveedores.count()

        return JsonResponse({
            'proveedores': list(proveedores_list),  # Convertimos el QuerySet a lista para JSON
            'has_next': has_next,
            'new_offset': offset + proveedores_por_click
        })

    # Paginación clásica para la carga inicial
    paginator = Paginator(proveedores, proveedores_por_pagina)
    try:
        proveedores_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        proveedores_paginados = paginator.page(1)
    except EmptyPage:
        proveedores_paginados = paginator.page(paginator.num_pages)

    return render(request, 'buscar_proveedores_por_categoria.html', {
        'categorias': categorias,
        'proveedores': proveedores_paginados,
        'categoria_seleccionada': categoria_seleccionada,
        'mensaje': mensaje,
        'offset': (page_number * proveedores_por_pagina)  # Se pasa el offset inicial
    })