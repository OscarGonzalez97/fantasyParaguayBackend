from django.shortcuts import render

from rest_framework import generics
from .models import Torneo, Jugador
from .serializers import TorneoSerializer, JugadorSerializer


class TorneoList(generics.ListAPIView):
    queryset = Torneo.objects.all()
    serializer_class = TorneoSerializer


class JugadorList(generics.ListAPIView):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer
