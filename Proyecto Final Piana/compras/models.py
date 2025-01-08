from django.db import models

class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=100)
    compras = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre_usuario}"

class Proveedor(models.Model):
    nombre_Proveedor = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_proveedor

class Producto(models.Model):
    nombre_Producto = models.CharField(max_length=100)
    descripcion = models.TextField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nombre_producto