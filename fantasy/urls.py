from django.urls import path, include
from .views import TorneoList, JugadorList, PartidoList, SyncJugador

urlpatterns = [
    path('api/', include([
        path('auth/', include('auth_fantasy.urls')),
        path('torneos/', TorneoList.as_view(), name='torneo-list'),
        path('jugadores/', JugadorList.as_view(), name='jugador-list'),
        path('partidos/', PartidoList.as_view(), name='partido-list'),
    ])),
    path('sincronizar-jugadores/', SyncJugador, name='sync-jugador'),
]
