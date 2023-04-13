from django.urls import path, include
from .views import TorneoList, JugadorList, PartidoList, SyncJugador, LigaList, LigaCreate

urlpatterns = [
    path('api/', include([
        path('auth/', include('auth_fantasy.urls')),
        path('torneos/', TorneoList.as_view(), name='torneo-list'),
        path('jugadores/', JugadorList.as_view(), name='jugador-list'),
        path('partidos/', PartidoList.as_view(), name='partido-list'),
        path('ligas/', include([
            path('', LigaList.as_view(), name='liga-list'),
            path('create/', LigaCreate.as_view(), name='liga-create'),
        ])),
    ])),
    path('sincronizar-jugadores/', SyncJugador, name='sync-jugador'),
]
