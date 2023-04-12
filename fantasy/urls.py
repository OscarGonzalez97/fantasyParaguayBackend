from django.urls import path, include
from .views import TorneoList, JugadorList, PartidoList

urlpatterns = [
    path('api/', include([
        path('torneos/', TorneoList.as_view(), name='torneo-list'),
        path('jugadores/', JugadorList.as_view(), name='jugador-list'),
        path('partidos/', PartidoList.as_view(), name='partido-list'),
    ])),
]
