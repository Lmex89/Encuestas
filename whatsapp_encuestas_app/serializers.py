from rest_framework import serializers

from .models import Encuesta, Codigo
from datetime import datetime, timedelta

URL = "https://encuestas.servicecloudlmex.co/encuestas/"
BITLY_URL = "https://bit.ly/3DFIsSO"


class CodigoSerializer(serializers.Serializer):
    codigo = serializers.IntegerField()
    vigencia = serializers.DateTimeField()
    valido = serializers.BooleanField()


class EncuestaSerializer(serializers.ModelSerializer):

    codigo_obj = CodigoSerializer(required=False)

    class Meta:
        model = Encuesta
        fields = ["descripcion", "data", "email", "codigo_obj"]

    def create(self, validated_data):

        encuesta = Encuesta.objects.create(**validated_data)
        codigo_obj = Codigo(
            vigencia=datetime.now() + timedelta(hours=24), encuesta=encuesta
        )
        encuesta.long_url = URL
        encuesta.bitly_url = BITLY_URL
        codigo_random = codigo_obj.create_codigo()
        codigo_obj.codigo = codigo_random
        codigo_obj.save()
        encuesta.save()
        return encuesta


class CodigoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Codigo
        fields = ["id", "vigencia", "codigo", "vigencia"]


class EncuestaDetailSerializer(serializers.ModelSerializer):

    codigo_obj = serializers.SerializerMethodField()

    class Meta:
        model = Encuesta
        fields = "__all__"

    def get_codigo_obj(self, instance):
        if not instance:
            return None
        codigo = Codigo.objects.filter(encuesta=instance.pk).first()
        return CodigoDetailSerializer(codigo).data
