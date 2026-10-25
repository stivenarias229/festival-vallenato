from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="panel"),
    path("categorias", views.categorias, name="panel_categorias"),
    path("votaciones", views.votaciones, name="panel_votaciones"),
    path("votaciones/<int:votacion_id>/opciones", views.opciones, name="panel_opciones"),
    path("usuarios", views.usuarios, name="panel_usuarios"),
    path("actividad", views.actividad, name="panel_actividad"),
]
