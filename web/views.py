from inertia import render


def home(request):
    return render(
        request,
        "Home",
        props={
            "app_name": "Aplicación",
        },
    )
