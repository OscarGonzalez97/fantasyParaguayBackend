from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Torneo, Jugador, Partido, Liga, EquipoUsuario, LigaUsuario, Equipo
from .serializers import TorneoSerializer, JugadorSerializer, PartidoSerializer, LigaSerializer, LigaCreateSerializer, \
    EquipoUsuarioSerializer, EquipoUsuarioCreateSerializer, LigaUsuarioCreateSerializer, BuscarJugadorSerializer

import requests

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
    # GET de la api rapid api
    # llamada a la API con ciclo for guardando la cantidad de pag y especificando pag actual = 1, fin del for
    # for de 2 hasta total de pag, 28
    # for de 2 a 28, request más nuevo parámetro de pag.
    url = "https://api-football-beta.p.rapidapi.com/players"
    querystring = {"season": "2023", "league": "250"}

    headers = {
        "X-RapidAPI-Key": "e1c42450b7mshfccc731f01303b8p1c67fcjsn808c5f34eae9",
        "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()
    pages = data["paging"]["total"]

    for player in data["response"]:
        posicion = player["statistics"][0]["games"]["position"]
        if posicion == 'Defender':
            posicion = "DEF"
        elif posicion == 'Midfielder':
            posicion = "MED"
        elif posicion == 'Goalkeeper':
            posicion = "POR"
        elif posicion == 'Attacker':
            posicion = "DEL"

        jugador = Jugador.objects.filter(id_api=int(player["player"]["id"])).first()
        try:
            equipo = Equipo.objects.filter(id_api=int(player["statistics"][0]["team"]["id"])).first()
        except Exception as e:
            equipo = None
        if not jugador:
            jugador = Jugador.objects.create(
                id_api=int(player["player"]["id"]),
                nombre_abreviado=player["player"]["name"][0:25],
                nombre=player["player"]["firstname"],
                apellido=player["player"]["lastname"],
                fecha_nacimiento=player["player"]["birth"]["date"],
                nacionalidad=player["player"]["nationality"],
                peso=float(player["player"]["weight"].split(" ")[0]) if player["player"]["weight"] else 0,
                altura=float(player["player"]["height"].split(" ")[0]) if player["player"]["height"] else 0,
                foto=player["player"]["photo"],
                posicion=posicion,
                lesionado=player["player"]["injured"],
                equipo=equipo if equipo else None
            )
            jugador.save()
        else:
            jugador.peso = float(player["player"]["weight"].split(" ")[0]) if player["player"]["weight"] else 0
            jugador.altura = float(player["player"]["height"].split(" ")[0]) if player["player"]["height"] else 0
            jugador.foto = player["player"]["photo"]
            jugador.posicion = posicion
            jugador.lesionado = player["player"]["injured"]
            jugador.save()

    # a partir del 1er request se empiezan a buscar todas las demas paginas
    for pagina in range(2, pages):
        url = "https://api-football-beta.p.rapidapi.com/players"
        querystring = {"season": "2023", "league": "250", "page": pagina}

        headers = {
            "X-RapidAPI-Key": "e1c42450b7mshfccc731f01303b8p1c67fcjsn808c5f34eae9",
            "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.json()

        for player in data["response"]:
            posicion = player["statistics"][0]["games"]["position"]
            if posicion == 'Defender':
                posicion = "DEF"
            elif posicion == 'Midfielder':
                posicion = "MED"
            elif posicion == 'Goalkeeper':
                posicion = "POR"
            elif posicion == 'Attacker':
                posicion = "DEL"

            jugador = Jugador.objects.filter(id_api=int(player["player"]["id"])).first()
            equipo = Equipo.objects.get(id_api=int(player["statistics"][0]["team"]["id"]))
            if not jugador:
                jugador = Jugador.objects.create(
                    id_api=int(player["player"]["id"]),
                    nombre_abreviado=player["player"]["name"][0:25],
                    nombre=player["player"]["firstname"],
                    apellido=player["player"]["lastname"],
                    fecha_nacimiento=player["player"]["birth"]["date"],
                    nacionalidad=player["player"]["nationality"],
                    peso=float(player["player"]["weight"].split(" ")[0]) if player["player"]["weight"] else 0,
                    altura=float(player["player"]["height"].split(" ")[0]) if player["player"]["height"] else 0,
                    foto=player["player"]["photo"],
                    posicion=posicion,
                    lesionado=player["player"]["injured"],
                    equipo=equipo if equipo else None
                )
                jugador.save()
            else:
                jugador.peso = float(player["player"]["weight"].split(" ")[0]) if player["player"]["weight"] else 0
                jugador.altura = float(player["player"]["height"].split(" ")[0]) if player["player"]["height"] else 0
                jugador.foto = player["player"]["photo"]
                jugador.posicion = posicion
                jugador.lesionado = player["player"]["injured"]
                jugador.save()

    return HttpResponse("Jugadores sincronizados!")


def SyncEquipo(request):
    url = "https://api-football-beta.p.rapidapi.com/teams"
    querystring = {"season": "2023", "league": "250"}

    headers = {
        "X-RapidAPI-Key": "e1c42450b7mshfccc731f01303b8p1c67fcjsn808c5f34eae9",
        "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()

    for equipo in data["response"]:
        team = Equipo.objects.filter(Q(id_api=int(equipo["team"]["id"])) | Q(nombre__icontains=equipo["team"]["name"]))
        if not team:
            equipo = Equipo.objects.create(
                id_api=int(equipo["team"]["id"]),
                nombre=equipo["team"]["name"],
                logo=equipo["team"]["logo"],
                pais="Paraguay",
                torneos=Torneo.objects.all().first()
            )
            equipo.save()

    return HttpResponse("Equipos sincronizados!")
