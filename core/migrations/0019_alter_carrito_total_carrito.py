# Generated by Django 5.0.4 on 2024-06-15 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_carrito_total_carrito'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrito',
            name='total_carrito',
            field=models.FloatField(default=0),
        ),
    ]