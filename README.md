# 🎵 LRCLIB — Consultor de Letras Urbanas

## Stakeholder

**Investigador cultural / estudiante de lingüística urbana latinoamericana**

Un investigador que estudia el slang, la jerga callejera y las expresiones culturales del reggaetón necesita una herramienta de línea de comandos que consulte letras de canciones en tiempo real, sin depender de plataformas comerciales con límites de uso o costos de suscripción.

---

## Propuesta de Valor — Problema / Solución

**Problema:** Las plataformas de letras (Genius, AZLyrics, Spotify) no ofrecen acceso programático gratuito. El investigador no puede automatizar consultas masivas ni integrarlas en pipelines de análisis.

**Solución:** Esta herramienta consulta [LRCLIB](https://lrclib.net) — una API pública, gratuita y sin API key — para extraer 5 campos de datos estructurados (nombre, artista, álbum, duración y letra) de cualquier canción, y los entrega por consola en formato legible y reproducible dentro de un contenedor Docker.

---

## Estructura del Repositorio

```
lrclib-letras/
├── app.py               # Script principal — consulta la API y procesa datos
├── build.sh             # Automatización: genera Dockerfile, construye y corre
├── requirements.txt     # Dependencias Python
├── .gitignore
├── README.md
└── evidencias/
    ├── docker/
    │   ├── output.txt       # docker ps -a + logs con datos reales de la API
    │   └── screenshot.png   # Captura de la salida en consola
    └── jenkins/
        ├── stage_view.png
        ├── console_output_build.png
        ├── credentials.png
        └── pipeline_script.txt
```

---

## Guía de Configuración — Variables de Entorno

La aplicación **no contiene credenciales hardcodeadas**. Toda configuración se pasa mediante variables de entorno:

| Variable       | Descripción                              | Valor por defecto       |
|----------------|------------------------------------------|-------------------------|
| `TRACK_NAME`   | Nombre de la canción a buscar            | `Titi Me Pregunto`      |
| `ARTIST_NAME`  | Nombre del artista                       | `Bad Bunny`             |
| `LRCLIB_URL`   | URL base de la API (opcional)            | `https://lrclib.net/api`|

### Configurar en Linux/Bash:
```bash
export TRACK_NAME="Gasolina"
export ARTIST_NAME="Daddy Yankee"
```

### Configurar en Windows/PowerShell:
```powershell
$env:TRACK_NAME = "Gasolina"
$env:ARTIST_NAME = "Daddy Yankee"
```

---

## Instrucciones de Ejecución con Docker

### Opción A — Script automatizado (recomendado)
```bash
chmod +x build.sh
bash build.sh
```
El script genera el `Dockerfile`, construye la imagen y ejecuta el contenedor automáticamente.

### Opción B — Comandos manuales
```bash
# 1. Construir la imagen
docker build -t lrclib-letras .

# 2. Ejecutar el contenedor (con canción personalizada)
docker run --name samplerunning \
  -e TRACK_NAME="Gasolina" \
  -e ARTIST_NAME="Daddy Yankee" \
  lrclib-letras

# 3. Ver estado del contenedor (debe mostrar Exited (0))
docker ps -a

# 4. Ver logs
docker logs samplerunning
```

---

## Manejo de Errores

El script maneja 4 tipos de errores de forma robusta:

| # | Tipo de Error        | Descripción                                      |
|---|----------------------|--------------------------------------------------|
| 1 | **Timeout**          | La API no responde en 10 segundos                |
| 2 | **ConnectionError**  | Sin red o DNS no resuelve el host                |
| 3 | **HTTP 404**         | Recurso no encontrado en la API                  |
| 4 | **Respuesta vacía**  | La API responde pero no retorna resultados JSON  |

---

## API Utilizada

- **LRCLIB** — [https://lrclib.net](https://lrclib.net)
- Pública, gratuita, sin API key requerida
- Endpoint usado: `GET /api/search?track_name=...&artist_name=...`
- Campos procesados: `trackName`, `artistName`, `albumName`, `duration`, `plainLyrics`
