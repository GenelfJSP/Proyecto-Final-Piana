# Generated by Django 5.1.4 on 2025-01-21 02:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0005_alter_producto_proveedor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proveedor',
            old_name='nombre_Proveedor',
            new_name='nombre',
        ),
        migrations.AlterField(
            model_name='producto',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.proveedor'),
        ),
    ]
