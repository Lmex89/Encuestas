from django.urls import path, re_path
from whatsapp_encuestas_app.views import (
    CodigoApiView,
    CodigoDetailApiView,
    EncuestaListCreateView,
    EncuestaLDetailView,
)


urlpatterns = [
    path("encuesta/", EncuestaListCreateView.as_view()),
    path(
        "encuesta/<int:pk>",
        EncuestaLDetailView.as_view(),
    ),
    path("codigos/", CodigoApiView.as_view()),
    path("codigos/<int:pk>", CodigoDetailApiView.as_view()),
]
