from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("catalogo.urls")),
    path("", include("cuentas.urls")),
    path("", include("votaciones.urls")),
    path("", include("resultados.urls")),
    path("panel/", include("panel.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("admin/", admin.site.urls)]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
