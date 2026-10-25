# Decisiones pendientes de validación

Cada ítem está implementado de forma configurable. El comentario `# PENDIENTE DE VALIDACIÓN (P-xx)` aparece junto al código.

| ID | Qué se asumió | Dónde está | Cómo cambiarlo |
|---|---|---|---|
| P-01 | Identificación por correo electrónico | `cuentas/identificacion.py` | Cambiar `obtener_identificador` |
| P-02 / P-08 | Cualquier usuario verificado y activo es elegible. Sin edad, ubicación ni nacionalidad | `votaciones/services.py` → `es_elegible` | Añadir reglas en esa función |
| P-03 | 1 voto por usuario y votación. El confirmado no se modifica | `catalogo.Votacion.limite_votos_por_usuario` y servicio de voto | Editar el campo en el panel |
| P-04 | Visibilidad por defecto `internos` | `catalogo.Votacion.visibilidad_resultados` | Editar la votación en el panel |
| P-05 | Jurados y votos ponderados no se implementan | — | No hay campo de peso |
| P-06 | Categorías oficiales no están quemadas. El seed es DEMO | `catalogo/management/commands/seed_demo.py` | Cargar datos reales desde el panel |
| P-07 | Nombre, correo, contraseña y consentimiento Ley 1581 | `cuentas.Usuario` y `RegistroForm` | Ampliar el formulario si el cliente lo pide |
| P-09 | Roles `votante` y `administrador`. MFA no se implementa | `cuentas/permissions.py` y `Usuario.rol` | Endurecer el decorador único |
| P-10 | Hosting no asumido. Todo por `.env` | `config/settings.py`, `.env.example` | Completar variables de producción |
| P-11 | Sin cifras inventadas. Índices, atomicidad y sin N+1 | modelos y servicios | Revisar consultas si hay picos reales |
| P-12 | El admin ve nombre, correo, rol, estado y fecha de registro | `panel/views.py` → `usuarios` | No agregar más campos a las props |
| CAPTCHA | Hook vacío que siempre pasa | `cuentas/captcha.py` | Implementar `captcha_ok` |
| RNF-03 | 5 intentos de login y bloqueo de 15 minutos | `LOGIN_MAX_INTENTOS`, `LOGIN_BLOQUEO_MINUTOS` | Variables de entorno |
