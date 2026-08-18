#INFORME TÉCNICO

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

## Arquitectura

## Seguridad

### ¿Qué puertos se exponen y por qué?

1. Puerto 5432: Expone la base de datos que se ejecuta dentro del contenedor.
2. Puerto 8000: Expone automáticamente una página interactiva con la documentación de todos sus endpoints.
3. Puerto 11434: Ollama descarga y ejecuta modelos de lenguaje en su propia máquina y los expone mediante una API REST.

### ¿Qué roles existen en la Base de Datos y que puede hacer cada uno?

Por seguridad, la aplicación nunca debe conectarse como administrador, por lo cual se crea un rol de APLICACIÓN con privilegios minimos:

* Hacer inferencias y consultas en las BD.
* No se conceden permisos de eliminación y actualización como son DELETE, UPDATE y DROP.

### ¿Cómo se manejan los secretos?

Al desplegar contenedores, pasar contraseñas directamente en la línea de comandos con -e POSTGRES_PASSWORD=... (como figura en el comando docker run) no es seguro, ya que la contraseña queda registrada en el historial de la terminal (history) y en la inspección del contenedor (docker inspect).

#### Buenas prácticas para el manejo de secretos:

1. Uso de archivos .env (Desarrollo local):

* Guardar variables en un archivo .env excluido del control de versiones (.gitignore).
* Pasar las variables a Docker mediante --env-file .env.

2. Docker Secrets / PostgreSQL Secret Files (Producción):

* Utilizar la variable POSTGRES_PASSWORD_FILE=/run/secrets/db_password.
* El secreto se almacena en un archivo cifrado en el host y se monta dentro del contenedor en tiempo de ejecución, evitando que la clave aparezca en texto plano en la configuración del contenedor.

3. Gestores de Secretos Externalizados:

* En entornos cloud o clusters, integrarse con herramientas como HashiCorp Vault, AWS Secrets Manager o Azure Key Vault.

### Gestión frente a un filtro de contraseñas

1. Rotación inmediata de credenciales.
2. Actualización de servicios/variables de entorno.
3. Terminar conexiones activas sospechosas.
4. Auditoría y revisión de logs.
5. Mitigación de la fuente de filtración por medio de identificación de la causa y toma de medidas correctivas.