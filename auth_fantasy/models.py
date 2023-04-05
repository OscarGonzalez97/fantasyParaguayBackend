from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    full_name = models.CharField('Nombre y Apellido', max_length=180, blank=True)


    class Meta:
        ordering = ['-is_active', 'username']

    def __str__(self):
        if not self.full_name:
            return self.username
        return self.full_name

    def save(self, *args, **kwargs):
        self.full_name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)
