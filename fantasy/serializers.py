from rest_framework import serializers
from .models import Jugador, Torneo, Partido


class TorneoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torneo
        fields = '__all__'


class JugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jugador
        fields = '__all__'


class PartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = '__all__'
