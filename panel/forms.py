from django import forms

from catalogo.models import Categoria, Edicion, Opcion, Votacion
from cuentas.models import Usuario


class EdicionForm(forms.ModelForm):
    class Meta:
        model = Edicion
        fields = ["nombre", "anio", "estado"]


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["edicion", "nombre", "descripcion", "estado", "icono"]


class VotacionForm(forms.ModelForm):
    class Meta:
        model = Votacion
        fields = [
            "categoria",
            "titulo",
            "fecha_inicio",
            "fecha_fin",
            "estado",
            "reglas",
            "visibilidad_resultados",
            "limite_votos_por_usuario",
        ]

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get("fecha_inicio")
        fin = cleaned.get("fecha_fin")
        if inicio and fin and fin <= inicio:
            raise forms.ValidationError("La fecha de cierre debe ser posterior al inicio.")
        return cleaned


class OpcionForm(forms.ModelForm):
    class Meta:
        model = Opcion
        fields = ["nombre", "descripcion", "imagen", "orden"]


class UsuarioAdminForm(forms.Form):
    rol = forms.ChoiceField(choices=Usuario.Rol.choices)
    estado = forms.ChoiceField(choices=Usuario.Estado.choices)
