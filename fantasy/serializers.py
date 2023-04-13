from rest_framework import serializers
from .models import Jugador, Torneo, Partido


class TorneoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torneo
        fields = '__all__'


class JugadorSerializer(serializers.ModelSerializer):
    equipo = serializers.StringRelatedField()

    class Meta:
        model = Jugador
        fields = '__all__'
        extra_kwargs = {
            'equipo': {'source': 'Equipo.nombre'}  # campo relacionado como el nombre en lugar del id
        }


class PartidoSerializer(serializers.ModelSerializer):
    equipo_local = serializers.StringRelatedField()
    equipo_visitante = serializers.StringRelatedField()
    class Meta:
        model = Partido
        fields = '__all__'
        extra_kwargs = {
            'equipo_local': {'source': 'Equipo.nombre'},
            'equipo_visitante': {'source': 'Equipo.nombre'}
        }
