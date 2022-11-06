from rest_framework import serializers

from .models import Encuesta, Codigo
from datetime import datetime, timedelta
class CodigoSerializer(serializers.Serializer):
    codigo = serializers.IntegerField()
    vigencia = serializers.DateTimeField()
    valido = serializers.BooleanField()

class EncuestaSerializer(serializers.ModelSerializer):

    codigo_obj = CodigoSerializer(required=False)

    class Meta:
        model = Encuesta
        fields = ['id','descripcion','data','email', 'codigo_obj']

    def create(self, validated_data):

        encuesta = Encuesta.objects.create(**validated_data)
        codigo_obj = Codigo(
            vigencia=datetime.now() + timedelta(hours=24),
            encuesta=encuesta
        )
        encuesta.long_url = f"https://www.servicecloudlmex.co/encuestas/{codigo_obj.id}"
        encuesta.bitly_url = f"bitly/demo"
        codigo_random = codigo_obj.create_codigo()
        codigo_obj.codigo = codigo_random
        codigo_obj.save()
        encuesta.save()
        return encuesta


class CodigoDetailSerializer( serializers.ModelSerializer):

    class Meta:
        model=Codigo
        fields = '__all__'

class EncuestaDetailSerializer(serializers.ModelSerializer):

    codigo_obj = CodigoDetailSerializer(read_only=True)

    class Meta:
        model = Encuesta
        fields = '__all__'