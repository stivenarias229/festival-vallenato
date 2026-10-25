# Trazabilidad pantalla → ruta → RF/CU

| Pantalla | Ruta | Vista | Página Vue | RF / CU |
|---|---|---|---|---|
| Inicio | `/` | `catalogo.views.inicio` | `Publico/Inicio` | CU-03 |
| Registro | `/registro` | `cuentas.views.registro` | `Auth/Registro` | CU-01, RF-01, RF-11 |
| Correo enviado | `/registro/enviado` | `cuentas.views.registro_enviado` | `Auth/RegistroEnviado` | RF-11 |
| Verificar correo | `/verificar/<uid>/<token>/` | `cuentas.views.verificar` | redirect | RF-11 |
| Iniciar sesión | `/ingresar` | `cuentas.views.ingresar` | `Auth/Ingresar` | CU-02, RF-02 |
| Cerrar sesión | `/salir` | `cuentas.views.salir` | redirect | RF-02 |
| Recuperar | `/recuperar` | `cuentas.views.recuperar` | `Auth/Recuperar` | RF-12 |
| Restablecer | `/recuperar/<uid>/<token>/` | `cuentas.views.restablecer` | `Auth/Restablecer` | RF-12 |
| Categorías | `/categorias` | `catalogo.views.categorias` | `Publico/Categorias` | CU-03, RF-03 |
| Votaciones | `/categorias/<id>/votaciones` | `catalogo.views.votaciones` | `Publico/Votaciones` | RF-03 |
| Detalle | `/votaciones/<id>` | `catalogo.views.detalle` | `Publico/Detalle` | RF-13 |
| Opciones | `/votaciones/<id>/opciones` | `catalogo.views.opciones` | `Publico/Opciones` | RF-13 |
| Confirmar | `/votaciones/<id>/confirmar` | `votaciones.views.confirmar` | `Votaciones/Confirmar` | RF-04, RF-14 |
| Votar | `POST /votaciones/<id>/votar` | `votaciones.views.votar` | redirect | CU-04, RB-01–04, RB-12 |
| Gracias | `/votaciones/<id>/gracias` | `votaciones.views.gracias` | `Votaciones/Gracias` | RF-15, RF-10 |
| Resultados públicos | `/votaciones/<id>/resultados` | `resultados.views.publicos` | `Resultados/Publicos` | CU-05, RF-10, RB-05 |
| Panel | `/panel` | `panel.views.inicio` | `Panel/Inicio` | RF-16 |
| Gestión categorías | `/panel/categorias` | `panel.views.categorias` | `Panel/Categorias` | RF-05, RF-06, CU-06 |
| Gestión votaciones | `/panel/votaciones` | `panel.views.votaciones` | `Panel/Votaciones` | RF-07, CU-07 |
| Gestión opciones | `/panel/votaciones/<id>/opciones` | `panel.views.opciones` | `Panel/Opciones` | RF-08 |
| Resultados admin | `/panel/resultados` | `resultados.views.admin` | `Panel/Resultados` | RF-09, CU-08 |
| Exportar CSV | `/panel/resultados/<id>/csv` | `resultados.views.exportar_csv` | archivo | RF-09 |
| Usuarios | `/panel/usuarios` | `panel.views.usuarios` | `Panel/Usuarios` | CU-09, RF-17, RF-18 |
| Actividad | `/panel/actividad` | `panel.views.actividad` | `Panel/Actividad` | RF-16 |
