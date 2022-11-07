from rest_framework import serializers

from .models import Encuesta, Codigo, Opcion, Pregunta
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
        fields = ["descripcion", "data", "email", "codigo_obj", "name"]

    def create(self, validated_data: dict) -> Encuesta:

        encuesta = Encuesta.objects.create(**validated_data)
        codigo_obj = Codigo(
            vigencia=datetime.now() + timedelta(hours=24), encuesta=encuesta
        )
        encuesta.long_url = URL
        encuesta.bitly_url = BITLY_URL
        codigo_random = codigo_obj.create_codigo()
        exist_codigo = Codigo.objects.filter(codigo=codigo_random, valido=True).exists()
        while exist_codigo:
            codigo_random = codigo_obj.create_codigo()
            exist_codigo = Codigo.objects.filter(
                codigo=codigo_random, valido=True
            ).exists()
        codigo_obj.codigo = codigo_random
        preguntas = validated_data["data"]

        for pregunta in preguntas:
            p = Pregunta.objects.create(
                pregunta_str=pregunta.get("pregunta"), encuesta=encuesta
            )
            opciones = pregunta.get("opciones")
            for opcion in opciones:
                Opcion.objects.create(pregunta=p, opcion_str=opcion)

        codigo_obj.save()
        encuesta.save()
        return encuesta


class CodigoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Codigo
        fields = ["id", "vigencia", "codigo", "vigencia"]


class OpcionesSerializer(serializers.ModelSerializer):

    opcion = serializers.SerializerMethodField()

    class Meta:
        model = Opcion
        fields = ["id", "opcion"]

    def get_opcion(self, instance):
        return instance.opcion_str


class PreguntaSerializer(serializers.ModelSerializer):

    opciones = serializers.SerializerMethodField()
    pregunta = serializers.SerializerMethodField()

    class Meta:
        model = Pregunta
        fields = ["id", "pregunta", "opciones"]

    def get_opciones(self, instance):

        return OpcionesSerializer(instance.opciones_x, many=True).data

    def get_pregunta(self, instance):
        return instance.pregunta_str


class EncuestaDetailSerializer(serializers.ModelSerializer):

    codigo_obj = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    def get_data(self, instance):
        preguntas_serializer = PreguntaSerializer(instance.pregunta_x, many=True)
        return preguntas_serializer.data

    def get_codigo_obj(self, instance):
        if not instance:
            return None
        codigo = Codigo.objects.filter(encuesta=instance.pk).first()
        return CodigoDetailSerializer(codigo).data

    class Meta:
        model = Encuesta
        fields = ["id", "data", "codigo_obj"]
