# MANUAL TÉCNICO

## Diagrama de Arquitectura

+-----------------------------------------------------------------------+
|                            CAPA DE CLIENTE                            |
|             [ Navegador Web / Postman / Pruebas de Carga k6 ]         |
+-----------------------------------------------------------------------+
                                   |
                                   | HTTP GET / POST (Puerto 8000)
                                   v
+-----------------------------------------------------------------------+
|                       CONTENEDOR / SERVICIO API                       |
|                       FastAPI (Puerto 8000)                           |
|                                                                       |
|   +---------------------------------------------------------------+   |
|   |                       MOTOR ECO (Interno)                     |   |
|   |          Evaluación mediante Expresiones Regulares            |   |
|   +---------------------------------------------------------------+   |
+-----------------------------------------------------------------------+
                |                                       |
                | HTTP /api/generate                    | TCP / SQL
                | (Puerto 11434)                        | (Puerto 5432)
                v                                       v
+-------------------------------+       +-------------------------------+
|      MOTOR DE INFERENCIA      |       |         BASE DE DATOS         |
|      Servidor Ollama          |       |     PostgreSQL 16 Alpine      |
|    (Puerto 11434)             |       |        (Puerto 5432)          |
|  Modelo: gemma3:270m          |       |    Base de datos: iadb       |
+-------------------------------+       +-------------------------------+

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