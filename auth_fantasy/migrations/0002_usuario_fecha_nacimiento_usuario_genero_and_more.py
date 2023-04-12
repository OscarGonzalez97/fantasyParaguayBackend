# Generated by Django 4.2 on 2023-04-12 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_fantasy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='genero',
            field=models.CharField(blank=True, choices=[('hombre', 'Hombre'), ('mujer', 'Mujer')], max_length=50, null=True, verbose_name='Géneros'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='nro_telefono',
            field=models.CharField(blank=True, null=True, verbose_name='Número de teléfono'),
        ),
    ]
