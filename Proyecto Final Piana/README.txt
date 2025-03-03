# Sistema de Compras

Este es un proyecto hecho en Django para la gestión de usuarios y contenido.

## Funcionalidades

-En todos los apartados se puede: (compras/Templates/base.html)

	-Iniciar sesion

	-Ir a "Inicio"

	-Ir a "Usuarios"

	-Ir a "Productos"

	-Ir a "Acerca de mi"


-En el apatado de "Inicio" se puede: (compras/Templates/inicio.html)

	-Ver las cards, que aparecen de forma aleatoria, de Categorias, Productos y Proveedores, con posibilidad de cargar mas hasta un maximo

		-Categorias, una categoria aleatoria, con el boton vamos a realizar la busqueda de esta card en "Buscar Productos por Categoría"

		-Productos, un producto aleatorio, con el boton vamos a realizar la busqueda de esta card en "Buscar Proveedores por Producto"

		-Proveedores, un proveedor aleatorio, con el boton vamos a realizar la busqueda de esta card en "Buscar Productos por Proveedor"

-En el apatado de "Usuarios" se puede: (usuarios/.....)

	-Crear usuario, no se debe estar logueado

	-Iniciar sesion con un usuario, no se debe estar logueado

		-Cambiar contraseña, no se debe estar logueado

	-Ver todos los usuarios, con dos tipos de botones

		-Eliminar usuario, no se debe estar logueado


-En el apatado de "Productos" se puede: (productos/.....)

	-Ir a "Agregar Producto", se debe estar logueado

	-Ir a "Agregar Proveedor", se debe estar logueado

	-Ir a "Ver todos los productos"

		-Ver todos los productos, con dos tipos de botones

		-Eliminar productos, se debe estar logueado

	-Ir a "Ver todos los proveedores"

		-Ver todos los proveedores, con dos tipos de botones

		-Agregar/Quitar Categoría, se debe estar logueado, con dos tipos de botones

			-Agregar Categoría

			-Quitar Categoría

			-Eliminar Categoría

		-Eliminar proveedores, se debe estar logueado y no debe tener prodcutos asociados


	-Ir a "Buscar productos por proveedor", con dos tipos de botones

	-Ir a "Buscar proveedores por producto", con dos tipos de botones

	-Ir a "Buscar productos por categoria", con dos tipos de botones

	-Ir a "Buscar proveedores por categoria", con dos tipos de botones

	-Ver las cards, que aparecen de forma aleatoria, de Categorias, Productos y Proveedores, con posibilidad de cargar mas hasta un maximo

		-Categorias, una categoria aleatoria, con el boton vamos a realizar la busqueda de esta card en "Buscar Productos por Categoría"

		-Productos, un producto aleatorio, con el boton vamos a realizar la busqueda de esta card en "Buscar Proveedores por Producto"

		-Proveedores, un proveedor aleatorio, con el boton vamos a realizar la busqueda de esta card en "Buscar Productos por Proveedor"


-Con "importar_datos.py" (importar_datos.py) se cargan los datos guardados en el excel Casos_de_prueba_template.xlsx (Casos_de_prueba_template.xlsx), las fotos deben ser "Vinculos" para poder ser correctamente guardadas (sobre la celda click derecho y "Vinculo)

