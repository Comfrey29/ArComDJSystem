import os
import pygame
import sys
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# -----------------------------
# CONFIGURACIÓ SPOTIFY
# -----------------------------
CLIENT_ID = "EL_TEUT_CLIENT_ID"
CLIENT_SECRET = "EL_TEUT_SECRET"

try:
    sp = Spotify(auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    ))
    print("✅ Connexió a Spotify OK")
except Exception as e:
    sp = None
    print("⚠️ No s'ha pogut connectar a Spotify:", e)

# -----------------------------
# CONFIGURACIÓ PYGAME
# -----------------------------
# Evita errors en entorns sense àudio
os.environ["SDL_AUDIODRIVER"] = "dummy"

pygame.init()

# Inicialitza àudio només si hi ha dispositiu
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    AUDIO_OK = True
    print("✅ Àudio inicialitzat")
except pygame.error:
    AUDIO_OK = False
    print("⚠️ No hi ha dispositiu d'àudio. Mode silenci activat.")

# Pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ArCom DJ System")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# -----------------------------
# BUCLE PRINCIPAL
# -----------------------------
running = True
font = pygame.font.SysFont(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibuixa fons
    screen.fill(BLACK)

    # Mostra missatge d'estat
    audio_text = "Àudio: OK" if AUDIO_OK else "Àudio: no disponible"
    spotify_text = "Spotify: OK" if sp else "Spotify: no connectat"

    audio_surface = font.render(audio_text, True, WHITE)
    spotify_surface = font.render(spotify_text, True, WHITE)

    screen.blit(audio_surface, (50, 50))
    screen.blit(spotify_surface, (50, 100))

    pygame.display.flip()

pygame.quit()
sys.exit()
