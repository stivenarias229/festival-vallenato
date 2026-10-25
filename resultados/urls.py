from django.urls import path

from . import views

urlpatterns = [
    path("votaciones/<int:votacion_id>/resultados", views.publicos, name="resultados_publicos"),
    path("panel/resultados", views.admin, name="panel_resultados"),
    path("panel/resultados/<int:votacion_id>/csv", views.exportar_csv, name="panel_resultados_csv"),
]
