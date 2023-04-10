from django.db import models
from auth_fantasy.models import Usuario


class Torneo(models.Model):
    """Torneos que se van a poder jugar"""
    TIPOS = (
        ('liga', 'Liga'),
        ('copa', 'Copa'),
    )
    anho = models.PositiveSmallIntegerField('Año')
    pais = models.CharField('Pais', max_length=50)
    tipo = models.CharField('Tipo', choices=TIPOS, max_length=50)
    nombre = models.CharField('Nombre torneo', max_length=20)
    activo = models.BooleanField('Activo', default=False)

    def __str__(self):
        return self.nombre + ' ' + str(self.anho)


class Equipo(models.Model):
    """Equipo especifico"""
    nombre = models.CharField('Nombre equipo', max_length=20)
    id_api = models.PositiveIntegerField('ID API')
    torneos = models.ForeignKey(Torneo, related_name='equipos', on_delete=models.CASCADE)
    logo = models.URLField('Logo URL', null=True, blank=True)
    logo_image = models.ImageField('Logo Imagen', null=True, blank=True)
    pais = models.CharField('Pais', max_length=20, default='Paraguay')

    def __str__(self):
        return self.nombre


class Jugador(models.Model):
    """Jugador con toda la información necesaria para el fantasy"""
    POSICION = (
        ('DEL', 'Delantero'),
        ('CEN', 'Mediocampista'),
        ('DEF', 'Defensa'),
        ('POR', 'Portero'),
    )
    id_api = models.PositiveIntegerField('ID API', unique=True, null=True, blank=True)
    nombre_abreviado = models.CharField('Nombre abreviado', max_length=16)
    nombre = models.CharField('Nombre', max_length=70)
    apellido = models.CharField('Apellido', max_length=70)
    posicion = models.CharField('Posicion', choices=POSICION, max_length=10)
    peso = models.DecimalField('Peso', decimal_places=2, max_digits=6, null=True, blank=True)
    altura = models.DecimalField('Altura', decimal_places=2, max_digits=6, null=True, blank=True)
    foto = models.URLField('Foto URL', null=True, blank=True)
    foto_image = models.ImageField('Foto Imagen', null=True, blank=True)
    nacionalidad = models.CharField('Nacionalidad', max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', null=True, blank=True)
    equipo = models.ForeignKey(Equipo, related_name='jugadores', on_delete=models.SET_NULL, null=True, blank=True)
    precio =models.PositiveSmallIntegerField('Precio', null=True, blank=True)

    def __str__(self):
        return self.nombre_abreviado + " " + self.posicion + " " + str(self.equipo)


class PuntuacionJugador(models.Model):
    """Puntuacion total de jugador por torneo"""
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='puntuaciones')
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='puntuaciones_jugadores')
    puntos = models.SmallIntegerField()

    class Meta:
        unique_together = ('jugador', 'torneo',)

    def __str__(self):
        return f'Puntuación de {self.jugador} en {self.torneo}: {self.puntuacion_total}'


class PuntuacionUsuario(models.Model):
    """Puntuacion total de usuario por torneo"""
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='puntuaciones')
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='puntuaciones_usuarios')
    puntos = models.SmallIntegerField()

    class Meta:
        unique_together = ('usuario', 'torneo',)

    def __str__(self):
        return f'Puntuación de {self.usuario} en {self.torneo}: {self.puntuacion_total}'


# class EquipoUsuario(models.Model):
#     """El equipo seleccionado(15 jugadores) por el usuario por torneo"""
#     usuario = models.ForeignKey(Usuario, related_name='equipos', on_delete=models.CASCADE)
#     torneo = models.ForeignKey(Torneo, related_name='equipos_usuarios', on_delete=models.CASCADE)
#     jugadores = models.ManyToManyField(Jugador, related_name='jugadores', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.usuario) + " " + str(self.torneo)


class Partido(models.Model):
    """Un partido especifico """
    fecha = models.DateField('Fecha', null=True, blank=True)
    timestamp = models.PositiveBigIntegerField('Epoch time', null=True, blank=True)
    timezone = models.CharField('Timezone', max_length=10, default='UTC')
    id_api = models.PositiveIntegerField('ID API', unique=True, null=True, blank=True)
    torneo = models.ForeignKey(Torneo, related_name='partidos', on_delete=models.CASCADE)
    equipo_local = models.ForeignKey(Equipo, related_name='partidos_local', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='partidos_visitante', on_delete=models.CASCADE)
    goles_local = models.PositiveSmallIntegerField('Goles equipo local', default=0)
    goles_visitane = models.PositiveSmallIntegerField('Goles equipo visitante', default=0)
    ganador_local = models.BooleanField('Ganador local', default=False)
    ganador_visitante = models.BooleanField('Ganador visitante', default=False)

    def __str__(self):
        return str(self.fecha) + " " + str(self.torneo) + " " + str(self.equipo_local) + "vs" + str(self.equipo_visitante)


# class Alineacion(models.Model):
#     """Alineacion de un partido especifico"""
#     partido = models.ForeignKey(Partido, related_name='alineaciones', on_delete=models.CASCADE)
#     usuario = models.OneToOneField(Usuario, related_name='usuario', on_delete=models.CASCADE)
#     torneo = models.OneToOneField(Torneo, related_name='torneo', on_delete=models.CASCADE)
#     jugadores = models.ManyToManyField(Jugador, related_name='jugadores', on_delete=models.CASCADE)

# Liga: varios usuarios, puntos x cada usuario, nombre, fecha de creacion
