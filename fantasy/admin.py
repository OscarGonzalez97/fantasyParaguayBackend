from django.contrib import admin
from .models import Jugador, Torneo, Equipo, Partido, Liga

admin.site.register(Jugador)
admin.site.register(Torneo)
admin.site.register(Equipo)
admin.site.register(Partido)
admin.site.register(Liga)
