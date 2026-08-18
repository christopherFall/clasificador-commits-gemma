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