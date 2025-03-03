from django import forms
from .models import Producto, Proveedor, Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_Producto', 'descripcion', 'proveedor', 'categoria', 'foto']

    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), required=True)
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=True)
    foto = forms.ImageField(required=False)  # Campo para subir imagen

class ProveedorForm(forms.ModelForm):
    # Campo para seleccionar una categoría existente
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False)
    # Campo para ingresar una nueva categoría
    nueva_categoria = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Proveedor
        fields = ['nombre', 'descripcion', 'categoria', 'nueva_categoria', 'logotipo']

    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get('categoria')
        nueva_categoria = cleaned_data.get('nueva_categoria')

        # Primero, validar que no se hayan enviado ambas opciones.
        if categoria and nueva_categoria:
            raise forms.ValidationError(
                'No puedes seleccionar una categoría existente y agregar una nueva al mismo tiempo.'
            )

        # Si no se seleccionó una categoría pero se proporcionó una nueva, se crea.
        if not categoria and nueva_categoria:
            categoria, created = Categoria.objects.get_or_create(nombre=nueva_categoria)
            cleaned_data['categoria'] = categoria

        return cleaned_data
