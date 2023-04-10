from django.shortcuts import render

from rest_framework import generics, filters
from .models import Torneo, Jugador
from .serializers import TorneoSerializer, JugadorSerializer
from django_filters.rest_framework import DjangoFilterBackend


class TorneoList(generics.ListAPIView):
    queryset = Torneo.objects.all()
    serializer_class = TorneoSerializer


class JugadorList(generics.ListAPIView):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['posicion']
