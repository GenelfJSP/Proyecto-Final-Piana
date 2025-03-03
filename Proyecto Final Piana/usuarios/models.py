from django.db import models

class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=100)
    compras = models.TextField(blank=True)
    def __str__(self):
        return f"{self.nombre_usuario}"