# Generated by Django 5.0.4 on 2024-05-23 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_mecanico_foto_mecanico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mecanico',
            name='foto_mecanico',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes/'),
        ),
    ]