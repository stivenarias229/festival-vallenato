from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ("email", "nombre", "rol", "estado", "verificado")
    ordering = ("email",)
    search_fields = ("email", "nombre")
    fieldsets = (
        (None, {"fields": ("email", "password", "nombre")}),
        ("Cuenta", {"fields": ("rol", "estado", "verificado")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "nombre", "password1", "password2"),
            },
        ),
    )
    filter_horizontal = ("groups", "user_permissions")
