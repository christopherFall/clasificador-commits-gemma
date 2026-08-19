# INFORME TÉCNICO

## Caracterización del modelo local

| Dato | Cómo obtenerlo | Valor |
| :--- | :--- | :--- |
| Perfil de hardware | Sección 2 de la guía | **Perfil Bajo / Entrada** (Intel HD Graphics, CPU 2 núcleos / 4 hilos @ 2.90 GHz, 8 GB RAM DDR4, SSD SATA) |
| RAM total del equipo | `free -h` | **3.8 GiB** (WSL) / **7.9 GB** (Host Windows) |
| Modelo y etiqueta | `ollama list` | **gemma3:270m** |
| Tamaño en disco | `ollama list` | **291 MB** |
| Latencia de 5 ejecuciones (ms) | `time curl ...` cinco veces | **75 ms, 14 ms, 8 ms, 10 ms, 10 ms** |
| Latencia promedio | Promedio de las cinco | **23.4 ms** |
| RAM usada durante la inferencia | `free -h` mientras responde | **492 MiB** (WSL) / **6.6 GB (84%)** (Host Windows) |
| Calidad percibida (1 a 5) | Su criterio, con una frase que lo justifique | **4 / 5** - Excelente tiempo de respuesta y bajo consumo de recursos, ideal para tareas livianas y equipos con hardware limitado. |

## Sección de pruebas

| ID | Tipo | Qué se verifica | Resultado esperado | Obtenido | Estado |
|---|---|---|---|---|---|
| P-01 | Funcional | GET `/health` responde | Código 200 y estado ok | `200 OK` (`test_health_responde_ok`) | PASSED |
| P-02 | Funcional | POST `/clasificar` con motor eco | Código 200 y tipo correcto | `200 OK` y tipo devuelto (`test_clasificar_eco_devuelve_tipo`) | PASSED |
| P-03 | Funcional | Motor inválido | Código 400 | `400 Bad Request` (`test_clasificar_rechaza_motor_invalido`) | PASSED |
| P-04 | Acceso | Rol `app_ia` intenta DROP TABLE | Error de permisos | `ERROR: must be owner of table inferencias` | PASSED |
| P-05 | Conectividad | La API resuelve el host `db` | Devuelve una IP interna | Resuelve a IP interna `172.19.0.2` | PASSED |
| P-06 | Disponibilidad | Reinicio del contenedor de BD | La API se recupera sola | Contenedor `db-ia` reiniciado y API responde `Healthy` | PASSED |
| P-07 | Persistencia | `down` y `up` conservan los datos | Los registros siguen existiendo | Registros conservados tras recrear contenedores (`docker compose down / up`) | PASSED |
| P-08 | Carga | 10 usuarios sobre el motor eco | p95 < 800 ms y errores < 5 % | `p95 = 56.6 ms` y `errores = 0.00%` (10 VUs en k6) | PASSED |
| P-09 | Caracterización | 10 inferencias con modelo | Promedio, mediana y p95 | *Pendiente por ejecución (Ollama)* | PENDIENTE |