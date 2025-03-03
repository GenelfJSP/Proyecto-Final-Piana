import pandas as pd

# Cargar las hojas de Excel
usuarios_df = pd.read_excel('Casos_de_prueba_template.xlsx', sheet_name='Registrar Usuarios')
proveedores_df = pd.read_excel('Casos_de_prueba_template.xlsx', sheet_name='Registrar Proveedores')
productos_df = pd.read_excel('Casos_de_prueba_template.xlsx', sheet_name='Registrar Productos')

# Mostrar un vistazo de cada dataframe para verificar que se cargaron correctamente
print(usuarios_df.head())
print(proveedores_df.head())
print(productos_df.head())
