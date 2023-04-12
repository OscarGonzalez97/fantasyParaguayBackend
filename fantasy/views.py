from django.shortcuts import render

from rest_framework import generics
from .models import Torneo, Jugador, Partido
from .serializers import TorneoSerializer, JugadorSerializer, PartidoSerializer


class TorneoList(generics.ListAPIView):
    queryset = Torneo.objects.all()
    serializer_class = TorneoSerializer


class JugadorList(generics.ListAPIView):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer


class PartidoList(generics.ListAPIView):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer

