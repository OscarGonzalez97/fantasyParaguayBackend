from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Usuario
from .serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Enpoint para crear un nuevo usuario (registro)"""
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'genero': user.genero,
            'fecha_nacimiento': user.fecha_nacimiento,
            'nro_telefono': user.nro_telefono,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginAuthToken(ObtainAuthToken):
    """Enpoint para el login"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'genero': user.genero,
            'fecha_nacimiento': user.fecha_nacimiento,
            'nro_telefono': user.nro_telefono,
        })


# request_schema_dict = openapi.Schema(
#     title=_("Update order"),
#     type=openapi.TYPE_OBJECT,
#     properties={
#         'ordered_items': openapi.Schema(type=openapi.TYPE_ARRAY, description=_('Ordered items list'),
#             items=openapi.Schema(type=openapi.TYPE_OBJECT, description=_('Ordered item'),
#                 properties={
#                     'item': openapi.Schema(type=openapi.TYPE_STRING, description=_('Item id'), example="123*123*0001"),
#                     'quantity': openapi.Schema(type=openapi.TYPE_NUMBER, description=_('Ordered quantity'), example=12.33),
#                     'sequence_number': openapi.Schema(type=openapi.TYPE_INTEGER,
#                     description=_('Sequence of item inclusion in the order.'), example=1),
#                     }
#             )
#         ),
#         'status': openapi.Schema(type=openapi.TYPE_STRING, description=_('Order status'), example=1, enum=[0,1,2,3,4,5]),
#         'invoicing_date': openapi.Schema(type=openapi.TYPE_STRING, description=_('Invoice date'),
#         example="2022-05-27T12:48:07.256Z", format="YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]"),
#         'invoice_number': openapi.Schema(type=openapi.TYPE_STRING, description=_('Invoice number'), example="123456789"),
#         'note': openapi.Schema(type=openapi.TYPE_STRING, description=_('Client user note'), example=_("Client user note")),
#         'agent_note': openapi.Schema(type=openapi.TYPE_STRING, description=_('Agent note'), example=_("Agent note")),
#     }
# )
#
# @swagger_auto_schema(request_body=request_schema_dict, responses={200: 'Order updated.'})
