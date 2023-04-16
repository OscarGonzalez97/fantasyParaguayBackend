from django.contrib import admin
from .models import Jugador, Torneo, Equipo, Partido, Liga, EquipoUsuario, LigaUsuario

admin.site.register(Jugador)
admin.site.register(Torneo)
admin.site.register(Equipo)
admin.site.register(Partido)
admin.site.register(Liga)
admin.site.register(EquipoUsuario)
admin.site.register(LigaUsuario)
