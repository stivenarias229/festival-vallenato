from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="panel"),
    path("categorias", views.categorias, name="panel_categorias"),
    path("votaciones/exportar", views.exportar_votaciones, name="panel_votaciones_exportar"),
    path("votaciones", views.votaciones, name="panel_votaciones"),
    path("votaciones/<int:votacion_id>/opciones", views.opciones, name="panel_opciones"),
    path("usuarios/exportar", views.exportar_usuarios, name="panel_usuarios_exportar"),
    path("usuarios", views.usuarios, name="panel_usuarios"),
    path("actividad/exportar", views.exportar_actividad, name="panel_actividad_exportar"),
    path("actividad", views.actividad, name="panel_actividad"),
]
