from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("categorias", views.categorias, name="categorias"),
    path("categorias/<int:categoria_id>/votaciones", views.votaciones, name="categoria_votaciones"),
    path("votaciones/<int:votacion_id>", views.detalle, name="votacion_detalle"),
    path("votaciones/<int:votacion_id>/opciones", views.opciones, name="votacion_opciones"),
]
