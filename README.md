# CLASIFICADOR DE MENSAJES DE COMMIT

Este es un proyecto integrador con el flujo completo de la industria: **repositorio Git, código, contenedores, integración continua, despliegue, pruebas documentación y publicación de una versión**. Es un clasificador de mensajes de commit: un servicio que recibe el texto de un commit y determina si corresponde a ***feat, fix, docs, test, chore o refactor***, usando un LLM local. Cada petición queda registrada en una base de datos **PostgreSQL**, todo contenerizado con **Docker** y validado por un **pipeline en GitHub Actions**. 

## Integrantes

Cristian David Ramirez Perez 
> Christopher Fall

## Perfil del hardware

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

## Requisitos minimos

**Compatibles con el ***perfil del hardware*** y la caracterización del modelo usado expuestos en el apartado anterior.**

## Instalación paso a paso 

1. **Actualizar el sistema e instalar dependencias base:**

´sudo apt update && sudo apt upgrade -y´
´sudo apt install -y git python3 python3-pip python3-venv curl´

2. **Clonar el repositorio:**

`git clone https://github.com/christopherFall/clasificador-commits-gemma.git`
`cd clasificador-commits-gemma`

3. **Crear y activar el entorno virtual de Python:**

`python3 -m venv .venv`
`source .venv/bin/activate`

4. **Instalar las dependencias del proyecto:**

`pip install --upgrade pip`
`pip install -r requirements.txt`

5. **Configurar las variables de entorno:**

Crea un archivo .env en la raíz del proyecto basándote en la plantilla:

DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_ADMIN_PASSWORD=
  
OLLAMA_URL=
MODELO_OLLAMA=
MOTOR_POR_DEFECTO=


6. **Desplegar los servicios con Docker Compose:**

`docker compose up -d`

## Verificar funcionamiento y endpoints

* Verifica estado de contenedores:

`docker compose ps`

1. Probar Endpoint `/health`:

`curl -X GET "http://localhost:8000/health"`
*Respuesta esperada*
> {
>  "estado": "ok",
>  "base_datos": "ok"
>}

2. Probar Endpoint `/clasificar`:

**MOTOR ECO**
`curl -X POST "http://localhost:8000/clasificar" \`
     `-H "Content-Type: application/json" \`
     `-d '{"texto": "corrige el error de login", "motor": "eco"}'`
*Respuesta esperada*
> {
>   "tipo": "fix",
>   "latencia_ms": 1.25
> }
**MOTOR OLLAMA**
`curl -X POST "http://localhost:8000/clasificar" \`
    ` -H "Content-Type: application/json" \`
    ` -d '{"texto": "agrega la documentacion de la api", "motor": "ollama"'`

3. Probar Endpoint `/inferencias`

`curl -X GET "http://localhost:8000/inferencias?limite=5"`
*Respuesta esperada*
> Lista en formato JSON con los registros parseados desde PostgreSQL.

## Solución de Problemas

1. Permiso denegado al interactuar con Docker

`permission denied while trying to connect to the Docker daemon socket`
*Causa:* El usuario de Linux no pertenece al grupo con privilegios para interactuar con el socket de Docker (/var/run/docker.sock).
*Solución:* 

> `sudo usermod -aG docker $USER`
> `newgrp docker`

2. Advertencia del Linter BLE001 por Captura Genérica de Excepciones

`BLE001: Do not catch blind exception: Exception`
*Causa:* Uso de `except Exception:` genérico en bloques de captura de errores, lo cual puede enmascarar fallos imprevistos del sistema.
*Solución:* Reemplazar la excepción genérica por la excepción específica del conector de la base de datos:

> import psycopg2
> from fastapi import HTTPException
> 
> try:
>     with conexion() as con:
>         ...
> except psycopg2.Error:
>     raise HTTPException(status_code=503, detail="Base de datos no disponible")
> 

3. Error HTTP 503 Service Unavailable durante Ejecución de Pruebas Unitarias

`AssertionError: assert 503 == 200` al ejecutar `pytest`
*Causa:* El endpoint `/health` intenta conectarse a PostgreSQL real en `localhost`, pero la base de datos no está activa o las variables de entorno de red difieren en el entorno de pruebas.
*Solución:* Implementar simulación (mocking) de la conexión en tests/test_api.py para aislar las pruebas unitarias:

> from unittest.mock import patch, MagicMock
> 
> def test_health_responde_ok():
>     with patch("app.main.conexion") as mock_conexion:
>         mock_con = MagicMock()
>         mock_cur = MagicMock()
>         mock_conexion.return_value.__enter__.return_value = mock_con
>         mock_con.cursor.return_value.__enter__.return_value = mock_cur
> 
>         r = cliente.get("/health")
>         assert r.status_code == 200

4. Fallo de Módulo No Encontrado al Ejecutar Pytest

`ModuleNotFoundError: No module named 'app'`
*Causa:* `pytest` no añade automáticamente el directorio raíz del proyecto al `sys.path` de Python.
*Solución:* Crear un archivo `pytest.ini` en la raíz del proyecto con la siguiente directiva:

> [pytest]
> pythonpath = .

5. Error JSONDecodeError en Script de Caracterización de Latencia

`requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` al ejecutar `caracterizar_modelo.py`
*Causa:* La API responde con un código de error HTTP (500 o 503) en formato texto/HTML en lugar de JSON debido a que el servicio Ollama no está en ejecución o la BD está inalcanzable.
*Solución:* 
1. Asegurar que el servidor Ollama y la base de datos estén corriendo antes de ejecutar la prueba.
2. Validar el código de respuesta HTTP antes de invocar .json() en el script de caracterización:

> r = requests.post("http://localhost:8000/clasificar", json={"texto": texto, "motor": "ollama"})
> if r.status_code != 200:
>     print(f"Error {r.status_code}: {r.text}")
>     continue
> datos = r.json()

HELP! :"V