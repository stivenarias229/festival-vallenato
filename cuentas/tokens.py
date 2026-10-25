from django.contrib.auth.tokens import PasswordResetTokenGenerator


class VerificacionCorreoToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{user.verificado}{user.email}{timestamp}"


token_verificacion = VerificacionCorreoToken()
