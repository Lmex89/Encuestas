from django.urls import path, re_path
from whatsapp_encuestas_app.views import EncuestaListCreateView, EncuestaLDetailView


urlpatterns = [
    path("encuesta/", EncuestaListCreateView.as_view()),
    path(
        "encuesta/<uuid:pk>",
        EncuestaLDetailView.as_view(),
    ),
]
