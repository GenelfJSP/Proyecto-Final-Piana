import os
import django
from django.core.files import File
import pandas as pd
from django.conf import settings

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SistemaComprasDjango.settings')
django.setup()

from django.contrib.auth.models import User
from productos.models import Proveedor, Producto, Categoria

# Ruta del archivo Excel (relativa a BASE_DIR)
file_path = os.path.join(BASE_DIR, 'Casos_de_prueba_template.xlsx')

# Cargar las hojas del Excel
df_usuarios = pd.read_excel(file_path, sheet_name='Registrar Usuarios')
df_proveedores = pd.read_excel(file_path, sheet_name='Registrar Proveedores')
df_productos = pd.read_excel(file_path, sheet_name='Registrar Productos')

# Filtra filas con valores vacíos en las columnas relevantes
df_usuarios = df_usuarios.dropna(subset=['nombre_usuario', 'contrasena'])
df_proveedores = df_proveedores.dropna(subset=['nombre'])
df_productos = df_productos.dropna(subset=['nombre_producto', 'proveedor'])

# Convertir las columnas de imágenes a cadenas y manejar valores vacíos
df_productos['foto'] = df_productos['foto'].astype(str)
df_productos['foto'] = df_productos['foto'].apply(lambda x: x if x.strip() and x != 'nan' else None)

df_proveedores['logotipo'] = df_proveedores['logotipo'].astype(str)
df_proveedores['logotipo'] = df_proveedores['logotipo'].apply(lambda x: x if x.strip() and x != 'nan' else None)

# Crear las carpetas de imágenes si no existen (rutas relativas)
FOTOS_DIR = os.path.join(BASE_DIR, 'media', 'productos', 'productos', 'fotos')
LOGOS_DIR = os.path.join(BASE_DIR, 'media', 'productos', 'proveedores', 'logos')
os.makedirs(FOTOS_DIR, exist_ok=True)
os.makedirs(LOGOS_DIR, exist_ok=True)
print(f"Carpeta de fotos creada o verificada: {FOTOS_DIR}")
print(f"Carpeta de logotipos creada o verificada: {LOGOS_DIR}")

# Registrar los usuarios
for index, row in df_usuarios.iterrows():
    if row['nombre_usuario'].strip():  # Asegúrate de que el nombre del usuario no esté vacío
        if not User.objects.filter(username=row['nombre_usuario']).exists():
            user = User.objects.create_user(
                username=row['nombre_usuario'],
                password=row['contrasena']
            )
            user.save()
            print(f"Usuario {row['nombre_usuario']} creado con éxito.")
        else:
            print(f"El usuario {row['nombre_usuario']} ya existe.")
    else:
        print(f"El usuario con nombre vacío no será creado.")

# Registrar los proveedores
for index, row in df_proveedores.iterrows():
    if row['nombre'].strip():  # Asegúrate de que el nombre del proveedor no esté vacío
        if not Proveedor.objects.filter(nombre=row['nombre']).exists():
            proveedor = Proveedor.objects.create(
                nombre=row['nombre'],
                descripcion=row['descripcion']
            )
            print(f"Proveedor {row['nombre']} creado con éxito.")

            # Agregar logotipo si existe una en el archivo Excel
            if row.get('logotipo') and row['logotipo'].strip() and row['logotipo'] != 'nan':
                logo_path = row['logotipo']
                if os.path.exists(logo_path):  # Verifica que el logotipo exista
                    with open(logo_path, 'rb') as img_file:
                        # Guarda la imagen en la carpeta correcta
                        proveedor.logotipo.save(
                            os.path.basename(logo_path),  # Nombre del archivo
                            File(img_file),  # Contenido del archivo
                            save=True  # Guarda el proveedor después de asignar el logotipo
                        )
                        print(f"Logotipo del proveedor {row['nombre']} cargado con éxito.")
                else:
                    print(f"El logotipo {logo_path} no existe para el proveedor {row['nombre']}.")
            else:
                print(f"No se especificó un logotipo válido para el proveedor {row['nombre']}.")
        else:
            print(f"El proveedor {row['nombre']} ya existe.")
    else:
        print(f"El proveedor con nombre vacío no será creado.")

# Registrar las categorías
for index, row in df_productos.iterrows():
    if row['categoria'].strip():  # Verificar que la categoría no esté vacía
        if not Categoria.objects.filter(nombre=row['categoria']).exists():
            categoria = Categoria.objects.create(nombre=row['categoria'])
            print(f"Categoría {row['categoria']} creada con éxito.")
        else:
            print(f"La categoría {row['categoria']} ya existe.")

# Registrar los productos
for index, row in df_productos.iterrows():
    if row['nombre_producto'].strip() and row['proveedor'].strip():  # Asegúrate de que el nombre del producto y proveedor no estén vacíos
        proveedores = Proveedor.objects.filter(nombre=row['proveedor'])
        if proveedores.count() == 1:
            proveedor = proveedores.first()
            try:
                # Buscar la categoría por nombre
                categoria = Categoria.objects.filter(nombre=row['categoria']).first()

                if categoria:  # Si la categoría existe
                    # Crear el producto
                    producto = Producto.objects.create(
                        nombre_Producto=row['nombre_producto'],
                        descripcion=row['descripcion'],
                        proveedor=proveedor,
                        categoria=categoria
                    )
                    print(f"Producto {row['nombre_producto']} creado con éxito con categoría {row['categoria']}.")

                    # Agregar foto si existe una en el archivo Excel
                    if row.get('foto') and row['foto'].strip() and row['foto'] != 'nan':
                        photo_path = row['foto']
                        if os.path.exists(photo_path):  # Verifica que la foto exista
                            with open(photo_path, 'rb') as img_file:
                                # Guarda la imagen en la carpeta correcta
                                producto.foto.save(
                                    os.path.basename(photo_path),
                                    File(img_file),
                                    save=True
                                )
                                print(f"Foto del producto {row['nombre_producto']} cargada con éxito.")
                        else:
                            print(f"La foto {photo_path} no existe para el producto {row['nombre_producto']}.")
                    else:
                        print(f"No se especificó una foto válida para el producto {row['nombre_producto']}.")
                else:
                    print(f"Categoría {row['categoria']} no encontrada para el producto {row['nombre_producto']}.")

            except Exception as e:
                print(f"Error al crear el producto {row['nombre_producto']}: {e}")
        elif proveedores.count() > 1:
            print(f"Error al crear el producto {row['nombre_producto']}: se encontraron múltiples proveedores con el nombre {row['proveedor']}.")
        else:
            print(f"Proveedor {row['proveedor']} no encontrado para el producto {row['nombre_producto']}.")
    else:
        print(f"El producto {row['nombre_producto']} o proveedor {row['proveedor']} tiene valores vacíos y no será creado.")