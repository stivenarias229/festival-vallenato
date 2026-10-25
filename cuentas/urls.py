from django.urls import path

from . import views

urlpatterns = [
    path("registro", views.registro, name="registro"),
    path("registro/enviado", views.registro_enviado, name="registro_enviado"),
    path("verificar/<uidb64>/<token>/", views.verificar, name="verificar_correo"),
    path("ingresar", views.ingresar, name="ingresar"),
    path("salir", views.salir, name="salir"),
    path("recuperar", views.recuperar, name="recuperar"),
    path("recuperar/<uidb64>/<token>/", views.restablecer, name="restablecer"),
]
