#!/bin/bash
# ─────────────────────────────────────────────────────────────
#  build.sh — Script de automatización
#  Genera el Dockerfile, construye la imagen y ejecuta el contenedor
# ─────────────────────────────────────────────────────────────

set -e   # detener ante cualquier error

IMAGE_NAME="lrclib-letras"
CONTAINER_NAME="samplerunning"

echo "=============================================="
echo "  PASO 1 — Generando Dockerfile"
echo "=============================================="

cat > Dockerfile <<'EOF'
# Imagen base ligera de Python
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY app.py .

# Variables de entorno con valores por defecto (se sobreescriben al correr)
ENV TRACK_NAME="Titi Me Pregunto"
ENV ARTIST_NAME="Bad Bunny"
ENV LRCLIB_URL="https://lrclib.net/api"

# Comando de ejecución
CMD ["python", "app.py"]
EOF

echo "[OK] Dockerfile generado."

echo ""
echo "=============================================="
echo "  PASO 2 — Construyendo imagen Docker"
echo "=============================================="
docker build -t ${IMAGE_NAME} .
echo "[OK] Imagen '${IMAGE_NAME}' construida."

echo ""
echo "=============================================="
echo "  PASO 3 — Ejecutando contenedor"
echo "=============================================="
docker run --name ${CONTAINER_NAME} \
  -e TRACK_NAME="Titi Me Pregunto" \
  -e ARTIST_NAME="Bad Bunny" \
  ${IMAGE_NAME}

echo ""
echo "=============================================="
echo "  PASO 4 — Estado del contenedor"
echo "=============================================="
docker ps -a --filter "name=${CONTAINER_NAME}"

echo ""
echo "[OK] Script completado exitosamente."
