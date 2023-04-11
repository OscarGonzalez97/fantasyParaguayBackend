from django.shortcuts import render
from rest_framework import generics, filters
from .models import Torneo, Jugador
from .serializers import TorneoSerializer, JugadorSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json



class TorneoList(generics.ListAPIView):
    queryset = Torneo.objects.all()
    serializer_class = TorneoSerializer


class JugadorList(generics.ListAPIView):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['posicion']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post (self, request):
        jd = json.loads(json.dumps(request.data))
        ''''Jugador.objects.create(id_api = jd["id_api"], nombre_abreviado = jd["nombre_abreviado"], nombre = jd["nombre"],
                                       apellido = jd["apellido"], posicion = jd["posicion"], peso = jd["peso"], altura = jd["altura"],
                                       foto = jd["foto"], foto_image = jd["foto_image"], nacionalidad = jd["nacionalidad"],
                                       fecha_nacimiento = jd["fecha_nacimiento"], precio = jd["precio"], equipo = jd["equipo"])'''

        datos = {'message': "Success"}
        return JsonResponse(datos)



