# Generated by Django 5.0.4 on 2024-06-23 01:47

import cloudinary.models
import core.funciones
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_mecanico_foto_mecanico_alter_trabajo_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trabajo',
            name='foto',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name=core.funciones.upload_to_mecanicos),
        ),
    ]
