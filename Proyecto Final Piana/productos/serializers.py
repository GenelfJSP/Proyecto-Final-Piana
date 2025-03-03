from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
    def validate_proveedor(self, value):
        # Si no hay proveedor, lanza un error
        if not value:
            raise ValidationError("Debe seleccionar un proveedor para este producto.")
        return value