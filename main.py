# main.py
import tkinter as tk
import pygame
import os

# inicialitza l'audio mixer amb paràmetres sensats
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

from ui.main_window import MainWindow
from spotify.spotify_requests import SpotifyRequests

def main():
    root = tk.Tk()
    # Posa aquí el teu token d'accés a Spotify si en tens (user token amb scopes)
    SPOTIFY_TOKEN = os.environ.get("ARCOM_SPOTIFY_TOKEN", "")
    spotify_client = SpotifyRequests(SPOTIFY_TOKEN) if SPOTIFY_TOKEN else None

    app = MainWindow(root, spotify_client)
    root.geometry("1000x600")
    root.mainloop()

if __name__ == "__main__":
    main()

