# core/deck.py
import os
import tempfile
import pygame

try:
    from pydub import AudioSegment
    USE_PYDUB = True
except Exception:
    USE_PYDUB = False

# IMPORTANT: call pygame.mixer.init(...) once from the app entrypoint
class Deck:
    """
    Deck encapsula una pista d'àudio local:
    - load(path) : carrega (converteix mp3->wav si cal)
    - play/pause/unpause/stop
    - set_volume(vol)  vol 0.0..1.0
    - is_playing()
    """
    def __init__(self, name: str, channel_id: int):
        self.name = name
        self.channel = pygame.mixer.Channel(channel_id)
        self.sound = None
        self.filepath = None
        self._tempfile = None
        self.paused = False
        self.vol = 1.0

    def load(self, path: str):
        self.unload_temp()
        self.filepath = path
        ext = os.path.splitext(path)[1].lower()
        if USE_PYDUB and ext in ('.mp3', '.aac', '.m4a', '.flac', '.wma', '.ogg'):
            seg = AudioSegment.from_file(path)
            tf = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            seg.export(tf.name, format="wav")
            tf.close()
            self._tempfile = tf.name
            self.sound = pygame.mixer.Sound(self._tempfile)
        else:
            self.sound = pygame.mixer.Sound(path)

    def play(self):
        if not self.sound:
            return
        self.channel.stop()
        self.channel.play(self.sound)
        self.paused = False

    def pause(self):
        if self.channel.get_busy():
            self.channel.pause()
            self.paused = True

    def unpause(self):
        try:
            self.channel.unpause()
        except Exception:
            pass
        self.paused = False

    def stop(self):
        self.channel.stop()
        self.paused = False

    def set_volume(self, vol: float):
        self.vol = max(0.0, min(1.0, float(vol)))
        self.channel.set_volume(self.vol)

    def unload_temp(self):
        if self._tempfile:
            try:
                os.unlink(self._tempfile)
            except Exception:
                pass
            self._tempfile = None

    def unload(self):
        self.stop()
        self.unload_temp()
        self.sound = None
        self.filepath = None

    def is_playing(self):
        return self.channel.get_busy() and not self.paused

