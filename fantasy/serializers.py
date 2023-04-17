from django.db.models import Sum
from rest_framework import serializers

from .models import Jugador, Torneo, Partido, Liga, EquipoUsuario, LigaUsuario


class TorneoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torneo
        fields = '__all__'


class BuscarJugadorSerializer(serializers.ModelSerializer):
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
    equipo_local_imagen = serializers.URLField(source='equipo_local.logo', read_only=True)
    equipo_visitante_imagen = serializers.URLField(source='equipo_visitante.logo', read_only=True)

    class Meta:
        model = Partido
        fields = '__all__'
        extra_kwargs = {
            'equipo_local': {'source': 'Equipo.nombre'},
            'equipo_visitante': {'source': 'Equipo.nombre'}
        }


class LigaSerializer(serializers.ModelSerializer):
    creado_por_nombre = serializers.CharField(source='creado_por.full_name', read_only=True)
    puntos_liga = serializers.SerializerMethodField()

    class Meta:
        model = Liga
        fields = '__all__'

    def get_puntos_liga(self, obj):
        puntos_liga = obj.usuarios.aggregate(total_puntos=Sum('ligausuario__puntos'))['total_puntos']
        if not puntos_liga:
            return 0
        return puntos_liga


class LigaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = ['nombre', 'privado']


class LigaUsuarioCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = LigaUsuario
        fields = ['liga', ]


class JugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jugador
        fields = ('id', 'nombre', 'apellido', 'posicion')


class EquipoUsuarioSerializer(serializers.ModelSerializer):
    jugadores = JugadorSerializer(many=True)

    class Meta:
        model = EquipoUsuario
        fields = ('id', 'usuario', 'torneo', 'jugadores', 'gasto_total', 'nombre_equipo')


class EquipoUsuarioCreateSerializer(serializers.ModelSerializer):
    jugadores = JugadorSerializer(many=True)

    class Meta:
        model = EquipoUsuario
        fields = ('jugadores', 'gasto_total', 'nombre_equipo')
