from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    GENEROS = (
        ('hombre', 'Hombre'),
        ('mujer', 'Mujer'),
    )
    full_name = models.CharField('Nombre y Apellido', max_length=180, blank=True)
    genero = models.CharField('Géneros', choices=GENEROS, max_length=50, null=True, blank=True)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', null=True, blank=True)
    nro_telefono = models.CharField('Número de teléfono', null=True, blank=True)


    class Meta:
        ordering = ['-is_active', 'username']

    def __str__(self):
        if not self.full_name:
            return self.username
        return self.full_name

    def save(self, *args, **kwargs):
        self.full_name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)
