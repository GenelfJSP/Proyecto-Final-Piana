# Generated by Django 5.1.5 on 2025-01-24 01:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_Producto', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.proveedor')),
            ],
        ),
    ]
