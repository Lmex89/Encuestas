from rest_framework import generics
from whatsapp_encuestas_app.serializers import (
    EncuestaDetailSerializer,
    EncuestaSerializer,
)

from .models import Encuesta, Opcion, Pregunta
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Prefetch


class EncuestaListCreateView(generics.ListCreateAPIView):

    queryset = Encuesta.objects.all()
    serializer_class = EncuestaSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        encuesta_id = Encuesta.objects.latest("-created_at")
        serializer = EncuestaDetailSerializer(Encuesta.objects.get(pk=encuesta_id.id))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EncuestaLDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Encuesta.objects.all()
    serializer_class = EncuestaDetailSerializer

    def get_queryset(self):
        queryset = Encuesta.objects.filter(pk=self.kwargs.get('pk')).prefetch_related(
            Prefetch(
                lookup='pregunta_set',
                queryset=Pregunta.objects.all().prefetch_related(
                    Prefetch(
                        lookup='opcion_set',
                        queryset=Opcion.objects.all(),
                        to_attr='opciones_x'
                    )
                ),
                to_attr='pregunta_x'
            )
        ).first()
        return  queryset

    def retrieve(self, request, *args, **kwargs):
        
        instance = self.get_queryset()
        serializer = EncuestaDetailSerializer(instance=instance).data

        return Response(serializer, status=status.HTTP_200_OK)
