from django.urls import path

from . import views

urlpatterns = [
    path("mis-votos", views.mis_votos, name="mis_votos"),
    path("votaciones/<int:votacion_id>/confirmar", views.confirmar, name="voto_confirmar"),
    path("votaciones/<int:votacion_id>/votar", views.votar, name="votar"),
    path("votaciones/<int:votacion_id>/gracias", views.gracias, name="voto_gracias"),
]
