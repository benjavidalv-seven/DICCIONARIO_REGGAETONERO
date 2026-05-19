import os
import sys
import requests

# ─────────────────────────────────────────────
# CONFIGURACIÓN — sin hardcoding de credenciales
# LRCLIB es una API pública que NO requiere API key.
# Las variables de entorno permiten personalizar la búsqueda.
# ─────────────────────────────────────────────
TRACK_NAME  = os.getenv("TRACK_NAME",  "Titi Me Pregunto")
ARTIST_NAME = os.getenv("ARTIST_NAME", "Bad Bunny")
BASE_URL    = os.getenv("LRCLIB_URL",  "https://lrclib.net/api")

def buscar_cancion(track, artist):
    """
    Consulta la API de LRCLIB y retorna los datos de la canción.
    Maneja 4 tipos de errores: 404, Timeout, Conexión, respuesta vacía.
    """
    url = f"{BASE_URL}/search"
    params = {"track_name": track, "artist_name": artist}

    print(f"\n{'='*55}")
    print("  LRCLIB — Consulta de Letras Urbanas")
    print(f"{'='*55}")
    print(f"  Buscando : {track}")
    print(f"  Artista  : {artist}")
    print(f"  Endpoint : {url}")
    print(f"{'='*55}\n")

    # ── Error tipo 1: Timeout ──────────────────────────────
    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.Timeout:
        print("[ERROR] Timeout: la API no respondió en 10 segundos.")
        sys.exit(1)

    # ── Error tipo 2: Conexión (sin red / DNS) ─────────────
    except requests.exceptions.ConnectionError as e:
        print(f"[ERROR] Conexión fallida: no se pudo alcanzar {BASE_URL}.")
        print(f"        Detalle: {e}")
        sys.exit(1)

    # ── Error tipo 3: HTTP 404 u otros códigos de error ───
    if response.status_code == 404:
        print("[ERROR] 404 — Recurso no encontrado en la API.")
        sys.exit(1)

    if not response.ok:
        print(f"[ERROR] HTTP {response.status_code} — respuesta inesperada de la API.")
        sys.exit(1)

    # ── Error tipo 4: Respuesta vacía / sin resultados ────
    try:
        data = response.json()
    except ValueError:
        print("[ERROR] La respuesta de la API no es JSON válido.")
        sys.exit(1)

    if not data:
        print(f"[ERROR] Sin resultados para '{track}' de '{artist}'.")
        sys.exit(1)

    return data[0]   # primer resultado más relevante


def mostrar_resultado(song):
    """
    Procesa e imprime ≥ 3 campos de datos obtenidos de la API.
    Campos: trackName, artistName, albumName, plainLyrics, duration.
    """
    # ── Campo 1: Nombre de la canción ─────────────────────
    nombre  = song.get("trackName",  "Desconocido")

    # ── Campo 2: Artista ──────────────────────────────────
    artista = song.get("artistName", "Desconocido")

    # ── Campo 3: Álbum ────────────────────────────────────
    album   = song.get("albumName",  "Desconocido")

    # ── Campo 4: Duración en segundos ────────────────────
    duracion = song.get("duration", 0)
    minutos  = int(duracion) // 60
    segundos = int(duracion) % 60

    # ── Campo 5: Letra (primeras 20 líneas) ───────────────
    letra_raw = song.get("plainLyrics") or song.get("syncedLyrics") or ""
    letra_raw = letra_raw.replace("\r\n", "\n")
    lineas    = [l for l in letra_raw.split("\n") if l.strip()]
    preview   = "\n  ".join(lineas[:20]) if lineas else "(letra no disponible)"

    print("┌─────────────────────────────────────────────────────┐")
    print("│           DATOS OBTENIDOS DE LA API                 │")
    print("├─────────────────────────────────────────────────────┤")
    print(f"│  [1] Canción  : {nombre:<36} │")
    print(f"│  [2] Artista  : {artista:<36} │")
    print(f"│  [3] Álbum    : {album:<36} │")
    print(f"│  [4] Duración : {minutos}m {segundos:02d}s{'':<33} │")
    print("├─────────────────────────────────────────────────────┤")
    print("│  [5] LETRA (primeras 20 líneas):                    │")
    print("│                                                     │")
    for linea in lineas[:20]:
        # truncar si excede el ancho
        linea_t = linea[:50]
        print(f"│  {linea_t:<51} │")
    print("└─────────────────────────────────────────────────────┘")
    print("\n[OK] Consulta completada exitosamente.\n")


if __name__ == "__main__":
    cancion = buscar_cancion(TRACK_NAME, ARTIST_NAME)
    mostrar_resultado(cancion)
