from rest_framework import generics
from whatsapp_encuestas_app.serializeras import (
    EncuestaDetailSerializer,
    EncuestaSerializer,
)

from .models import Encuesta
from rest_framework import status
from rest_framework.response import Response


class EncuestaListCreateView(generics.ListCreateAPIView):

    queryset = Encuesta.objects.all()
    serializer_class = EncuestaSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        encuesta_id = response.data.get("id")
        serializer = EncuestaDetailSerializer(Encuesta.objects.get(pk=encuesta_id))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EncuestaLDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Encuesta.objects.all()
    serializer_class = EncuestaDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)