from rest_framework import serializers
from .models import Jugador, Torneo, Partido, Liga


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
    torneo_nombre = serializers.CharField(source='torneo.nombre', read_only=True)

    class Meta:
        model = Partido
        fields = '__all__'
        extra_kwargs = {
            'equipo_local': {'source': 'Equipo.nombre'},
            'equipo_visitante': {'source': 'Equipo.nombre'}
        }


class LigaSerializer(serializers.ModelSerializer):
    creado_por_nombre = serializers.CharField(source='creado_por.full_name', read_only=True)
    class Meta:
        model = Liga
        fields = '__all__'



class LigaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = ['nombre', 'privado']
