from django.db import models
from django.contrib.auth.models import AbstractUser
import random

# Create your models here.


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    visible = models.BooleanField(default=True)

    def soft_delete(self):
        """soft  delete a model instance"""
        self.visible = False
        self.save()

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class CustomUser(AbstractUser, BaseModel):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username


class Email(BaseModel):
    email = models.EmailField()

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "email",
                ]
            ),
        ]


class UserRegistration(BaseModel):
    email = models.ForeignKey(Email, null=False, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True
    )
    password = models.CharField(max_length=512, null=True, blank=True)


class Encuesta(BaseModel):

    name = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=254, null=True, blank=True)
    data = models.JSONField(null=True)
    email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.DO_NOTHING)
    long_url = models.URLField(null=True)
    bitly_url = models.CharField(max_length=254, null=True)


class Codigo(BaseModel):
    vigencia = models.DateTimeField(null=True)
    codigo = models.IntegerField(null=True)
    valido = models.BooleanField(default=True)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.DO_NOTHING)

    def create_codigo(
        self,
    ):
        return random.randint(1000, 9999)

    class Meta:
        unique_together = ("codigo", "id")


class Pregunta(BaseModel):

    encuesta = models.ForeignKey(Encuesta, on_delete=models.DO_NOTHING)
    pregunta_str = models.CharField(max_length=254)


class Opcion(BaseModel):

    pregunta = models.ForeignKey(Pregunta, on_delete=models.DO_NOTHING)
    opcion_str = models.CharField(max_length=254)


class Votos(BaseModel):

    encuesta = models.ForeignKey(Encuesta, on_delete=models.DO_NOTHING)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.DO_NOTHING)
    opcion = models.ForeignKey(Opcion, on_delete=models.DO_NOTHING)
    voto = models.IntegerField(default=1)
