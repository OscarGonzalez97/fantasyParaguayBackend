from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Torneo, Jugador, Partido, Liga, EquipoUsuario, LigaUsuario
from .serializers import TorneoSerializer, JugadorSerializer, PartidoSerializer, LigaSerializer, LigaCreateSerializer, \
    EquipoUsuarioSerializer, EquipoUsuarioCreateSerializer, LigaUsuarioCreateSerializer, BuscarJugadorSerializer


class TorneoList(generics.ListAPIView):
    queryset = Torneo.objects.all()
    serializer_class = TorneoSerializer


class JugadorList(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = Jugador.objects.exclude(equipo=None)
    serializer_class = BuscarJugadorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['posicion', 'equipo__nombre']

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre_equipo = self.request.query_params.get('equipo__nombre', None)
        if nombre_equipo is not None:
            queryset = queryset.filter(equipo__nombre__icontains=nombre_equipo)
        return queryset


class PartidoList(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer


class LigaList(generics.ListAPIView):
    """Listar todas las ligas"""
    permission_classes = [AllowAny]

    queryset = Liga.objects.all()
    serializer_class = LigaSerializer


class LigaCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Liga.objects.all()
    serializer_class = LigaCreateSerializer

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)


class LigaUnirme(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = LigaUsuario.objects.all()
    serializer_class = LigaUsuarioCreateSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class EquipoUsuarioList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EquipoUsuarioSerializer

    def get_queryset(self):
        user = self.request.user
        # todo: por ahora solo va poder traer un equipo el del unico torneo, esto va cambiar despues
        queryset = EquipoUsuario.objects.filter(usuario=user, torneo=Torneo.objects.all().first())
        return queryset


class EquipoUsuarioCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = EquipoUsuario.objects.all()
    serializer_class = EquipoUsuarioCreateSerializer

    def perform_create(self, serializer):
        # todo: torneo fijo temporalmente, mas adelante podra haber mas de un torneo o se va mandar como param
        serializer.save(creado_por=self.request.user, torneo=Torneo.objects.all().first())


def SyncJugador(request):
    #GET de la api rapid api
    # ir guardanado todo en nuestro modelo Juagdor
    # Jugador.objects.create()
    return HttpResponse("Jugadores sincronizados!")
