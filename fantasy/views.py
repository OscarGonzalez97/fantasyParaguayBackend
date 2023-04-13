from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny

from .models import Torneo, Jugador, Partido
from .serializers import TorneoSerializer, JugadorSerializer, PartidoSerializer


class TorneoList(generics.ListAPIView):
    queryset = Torneo.objects.all()
    serializer_class = TorneoSerializer


class JugadorList(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = Jugador.objects.exclude(equipo=None)
    serializer_class = JugadorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['posicion']


class PartidoList(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer


def SyncJugador(request):
    #GET de la api rapid api
    # ir guardanado todo en nuestro modelo Juagdor
    # Jugador.objects.create()
    return HttpResponse("Jugadores sincronizados!")
