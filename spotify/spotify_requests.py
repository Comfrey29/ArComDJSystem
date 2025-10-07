# spotify/spotify_requests.py
import requests
import json
from typing import Optional, Tuple

class SpotifyRequests:
    """
    Control bàsic via HTTP requests. Requereix un OAuth token amb scopes:
      - user-modify-playback-state
      - user-read-playback-state
    El token l'obtens via OAuth manual (Spotipy facilita això) o via la Consola de Spotify.
    """
    def __init__(self, token: str):
        self.token = token
        self.base = "https://api.spotify.com/v1/me/player"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _update_token(self, token: str):
        self.token = token
        self.headers["Authorization"] = f"Bearer {token}"

    def play_track(self, uri: str, device_id: Optional[str] = None) -> Tuple[int, str]:
        data = {"uris": [uri]}
        url = f"{self.base}/play"
        if device_id:
            url += f"?device_id={device_id}"
        r = requests.put(url, json=data, headers=self.headers)
        return r.status_code, r.text

    def pause(self, device_id: Optional[str] = None) -> Tuple[int, str]:
        url = f"{self.base}/pause"
        if device_id:
            url += f"?device_id={device_id}"
        r = requests.put(url, headers=self.headers)
        return r.status_code, r.text

    def resume(self, device_id: Optional[str] = None) -> Tuple[int, str]:
        url = f"{self.base}/play"
        if device_id:
            url += f"?device_id={device_id}"
        r = requests.put(url, headers=self.headers)
        return r.status_code, r.text

    def next(self, device_id: Optional[str] = None) -> Tuple[int, str]:
        url = f"{self.base}/next"
        if device_id:
            url += f"?device_id={device_id}"
        r = requests.post(url, headers=self.headers)
        return r.status_code, r.text

    def previous(self, device_id: Optional[str] = None) -> Tuple[int, str]:
        url = f"{self.base}/previous"
        if device_id:
            url += f"?device_id={device_id}"
        r = requests.post(url, headers=self.headers)
        return r.status_code, r.text

    def current_playback(self) -> Tuple[int, str]:
        r = requests.get(f"{self.base}", headers=self.headers)
        return r.status_code, r.text

