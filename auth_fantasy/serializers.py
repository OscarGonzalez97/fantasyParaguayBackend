from rest_framework import serializers

from auth_fantasy.models import Usuario


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'email', 'password', 'genero', 'fecha_nacimiento', 'nro_telefono', 'full_name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        user = Usuario.objects.create(
            email=validated_data['email'],
            genero=validated_data['genero'],
            fecha_nacimiento=validated_data['fecha_nacimiento'],
            nro_telefono=validated_data['nro_telefono'],
            first_name=validated_data['full_name'],
            last_name='',
            full_name=validated_data['full_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.genero = validated_data.get('genero', instance.genero)
        instance.fecha_nacimiento = validated_data.get('fecha_nacimiento', instance.fecha_nacimiento)
        instance.nro_telefono = validated_data.get('nro_telefono', instance.nro_telefono)
        instance.first_name = validated_data.get('full_name', instance.first_name)
        instance.last_name = validated_data.get('', instance.last_name)
        instance.full_name = validated_data.get('full_name', instance.last_name)
        instance.save()
        return instance
