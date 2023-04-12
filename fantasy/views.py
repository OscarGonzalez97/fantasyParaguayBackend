from django.shortcuts import render

from rest_framework import generics
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


class PartidoList(generics.ListAPIView):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer

