from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='categorias/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categorias = models.ManyToManyField(Categoria, related_name='proveedores')
    fecha_creacion = models.DateField(auto_now_add=True)
    logotipo = models.ImageField(upload_to='productos/proveedores/logos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre_Producto = models.CharField(max_length=100)
    descripcion = models.TextField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=False, blank=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=False, blank=False)
    fecha_publicacion = models.DateField(auto_now_add=True)
    foto = models.ImageField(upload_to='productos/productos/fotos', null=True, blank=True)

    def esta_disponible(self):
        return self.fecha_publicacion <= timezone.now().date()

    def clean(self):
        if not self.proveedor:
            raise ValidationError("El producto debe tener un proveedor asociado.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_Producto