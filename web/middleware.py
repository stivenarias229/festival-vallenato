from inertia import share

from web.json_body import cargar_json_en_post
from web.share import flash_compartido, urls_compartidas, usuario_compartido


class InertiaJsonMiddleware:
    """Rellena request.POST con el JSON que envía @inertiajs/vue3."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cargar_json_en_post(request)
        return self.get_response(request)


class InertiaShareMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        share(
            request,
            auth={"user": usuario_compartido(request)},
            flash=flash_compartido(request),
            urls=urls_compartidas(request),
        )
        return self.get_response(request)
