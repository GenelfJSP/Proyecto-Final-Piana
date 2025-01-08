from django import forms
from .models import Usuario
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import logout
from .forms import EliminarUsuarioForm
from .models import Producto, Proveedor
from django.contrib.auth.models import User
from .forms import RestablecerContraseñaForm
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from .forms import ClienteForm, BuscarClienteForm
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


def inicio(request):
    print("Se está cargando la vista de inicio")
    return render(request, 'inicio.html')

class FormularioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

def registrar_usuario(request):
    if request.method == 'POST':
        form = FormularioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}!')
            return redirect('iniciar_sesion')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = FormularioForm()
    return render(request, 'registrar_usuario.html', {'form': form})

def eliminar_usuario(request):
    if request.method == 'POST':
        form = EliminarUsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    user_to_delete = User.objects.get(username=username)
                    user_to_delete.delete()
                    messages.success(request, f"Usuario {username} eliminado con éxito.")
                    return redirect('listar_usuarios')
                except User.DoesNotExist:
                    messages.error(request, "El usuario no existe.")
            else:
                messages.error(request, "Credenciales incorrectas.")
        else:
            messages.error(request, "Por favor, corrija los errores en el formulario.")
    else:
        form = EliminarUsuarioForm()
    return render(request, 'compras/eliminar_usuario.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Has iniciado sesión correctamente')
                return redirect('usuarios')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Ingreselo correctamente')
    else:
        form = AuthenticationForm()
    return render(request, 'iniciar_sesion.html', {'form': form})

def inicio(request):
    return render(request, 'inicio.html')

def cerrar_sesion(request):
    logout(request)
    messages.success(request, "Sesión cerrada exitosamente.")
    return redirect('inicio')

def reestablecimiento_contraseña(request):
    if request.method == "POST":
        form = RestablecerContraseñaForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            nueva_contraseña = form.cleaned_data['nueva_contraseña']
            try:
                user = User.objects.get(username=username)
                user.set_password(nueva_contraseña)
                user.save()
                messages.success(request, f"Contraseña cambiada con éxito. Usuario: {username}.")
                return redirect('iniciar_sesion')
            except User.DoesNotExist:
                messages.error(request, "El nombre de usuario no existe.")
    else:
        form = RestablecerContraseñaForm()
    return render(request, 'reestablecimiento_contraseña.html', {'form': form})

def usuarios(request):
    print("Se está cargando la vista de usuarios")
    return render(request, 'compras/usuarios.html')

def listar_usuarios(request):
    usuarios = User.objects.all()
    print("Se está cargando la vista de los usuarios")
    return render(request, 'compras/listar_usuarios.html', {'usuarios': usuarios})

def listar_proveedores(request):
    print("Se está cargando la vista del listado de proveedores")
    proveedores = Proveedor.objects.all()
    return render(request, 'compras/listar_proveedores.html', {'proveedores': proveedores})

def eliminar_proveedor(request, proveedor_id):
    proveedor = Proveedor.objects.get(id=proveedor_id)
    if proveedor.productos.count() == 0:  # Solo elimina si no hay productos asociados
        proveedor.delete()
    else:
        # Si hay productos, no se puede eliminar
        return render(request, 'compras/error_eliminar_proveedor.html', {'proveedor': proveedor})
    return redirect('listar_proveedores')

def buscar_proveedor(request):
    print("Buscando proveedor...")
    proveedores = Proveedor.objects.all()
    return render(request, 'compras/buscar_proveedor.html', {'proveedores': proveedores})

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre_Proveedor', 'descripcion']

def productos(request):
    print("Se está cargando la vista de productos")
    return render(request, 'compras/productos.html')

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'compras/listar_productos.html', {'productos': productos})

def eliminar_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    producto.delete()
    return redirect('listar_productos')

def productos_por_proveedor(request, proveedor_id):
    proveedor = Proveedor.objects.get(id=proveedor_id)
    productos = Producto.objects.filter(proveedor=proveedor)
    return render(request, 'compras/productos_por_proveedor.html', {'proveedor': proveedor, 'productos': productos})

class ProductoForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), required=True)
    class Meta:
        model = Producto
        fields = ['nombre_Producto', 'descripcion', 'proveedor']

def agregar_producto(request):
    if request.method == 'POST':
        form_producto = ProductoForm(request.POST)
        form_proveedor = ProveedorForm(request.POST)
        if form_producto.is_valid() and form_proveedor.is_valid():
            proveedor = form_proveedor.save()
            producto = form_producto.save(commit=False)
            producto.proveedor = proveedor
            producto.save()
            return redirect('nombre_de_la_vista_donde_rediriges')
    else:
        form_producto = ProductoForm()
        form_proveedor = ProveedorForm()
    return render(request, 'compras/agregar_producto.html', {'form_producto': form_producto, 'form_proveedor': form_proveedor})

def buscar_productos_por_proveedor(request):
    proveedores = Proveedor.objects.all()
    productos = None
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        proveedor = Proveedor.objects.get(id=proveedor_id)
        productos = Producto.objects.filter(proveedor=proveedor)
    return render(request, 'compras/buscar_productos_por_proveedor.html', {'proveedores': proveedores, 'productos': productos})

def buscar_proveedores_por_producto(request):
    productos = Producto.objects.all()
    proveedores = None
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        producto = Producto.objects.get(id=producto_id)
        proveedores = producto.proveedor.all()
    return render(request, 'compras/buscar_proveedores_por_producto.html', {'productos': productos, 'proveedores': proveedores})
