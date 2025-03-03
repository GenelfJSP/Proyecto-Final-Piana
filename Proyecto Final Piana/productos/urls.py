from django.urls import path
from .views import (
    ListarProveedoresView, 
    AgregarProveedorView, 
    EliminarProveedorView, 
    ListarProductosView, 
    AgregarProductoView, 
    EliminarProductoView,
    ProductosView,
    AgregarQuitarCategoriaProveedorView,
    EliminarCategoriasView
)
from . import views

urlpatterns = [
    path('listar_proveedores/', ListarProveedoresView.as_view(), name='listar_proveedores'),  # Listar proveedores
    path('agregar_proveedor/', AgregarProveedorView.as_view(), name='agregar_proveedor'),  # Agregar proveedor
    path('proveedor/<int:proveedor_id>/eliminar/', EliminarProveedorView.as_view(), name='eliminar_proveedor'),  # Eliminar proveedor
    path('listar_productos/', ListarProductosView.as_view(), name='listar_productos'),  # Listar productos
    path('agregar_producto/', AgregarProductoView.as_view(), name='agregar_producto'),  # Agregar producto
    path('', ProductosView.as_view(), name='productos'),  # Vista principal de productos
    path('producto/<int:pk>/eliminar/', EliminarProductoView.as_view(), name='eliminar_producto'),  # Eliminar producto
    path('buscar_productos_por_proveedor/', views.buscar_productos_por_proveedor, name='buscar_productos_por_proveedor'),
    path('buscar_proveedores_por_producto/', views.buscar_proveedores_por_producto, name='buscar_proveedores_por_producto'),
    path('productos/agregar_categoria_proveedor/<int:proveedor_id>/', AgregarQuitarCategoriaProveedorView.as_view(), name='agregar_categoria_proveedor'),
    path('eliminar_categoria/<int:proveedor_id>/<int:categoria_id>/', EliminarCategoriasView.as_view(), name='eliminar_categoria'),
    path('buscar_productos_por_categoria/', views.buscar_productos_por_categoria, name='buscar_productos_por_categoria'),
    path('buscar_proveedores_por_categoria/', views.buscar_proveedores_por_categoria, name='buscar_proveedores_por_categoria'),
]

