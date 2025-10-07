# ui/main_window.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os

from core.deck import Deck
from core.audio_utils import equal_power_crossfade

class MainWindow:
    def __init__(self, root, spotify_client=None):
        self.root = root
        self.spotify = spotify_client
        root.title("ArCom DJ System - Prototype")
        self.deck_a = Deck("Deck A", 0)
        self.deck_b = Deck("Deck B", 1)
        self._build_ui()
        self._update_loop()

    def _build_ui(self):
        frm = ttk.Frame(self.root, padding=8)
        frm.pack(fill="both", expand=True)

        # Deck frames
        left = ttk.Frame(frm)
        left.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        right = ttk.Frame(frm)
        right.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)

        # Deck A
        self._deck_panel(left, self.deck_a)
        # Deck B
        self._deck_panel(right, self.deck_b)

        # Crossfader
        cross_frame = ttk.LabelFrame(frm, text="Crossfader")
        cross_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=8)
        self.cross_var = tk.DoubleVar(value=0.5)
        slider = ttk.Scale(cross_frame, from_=0.0, to=1.0, orient="horizontal",
                           variable=self.cross_var, command=self._on_cross)
        slider.pack(fill="x", padx=6, pady=6)

        # Spotify area
        if self.spotify:
            sp_frame = ttk.LabelFrame(frm, text="Spotify")
            sp_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=6)
            self.sp_uri = tk.StringVar()
            ttk.Entry(sp_frame, textvariable=self.sp_uri, width=60).grid(row=0, column=0, padx=6, pady=6)
            ttk.Button(sp_frame, text="Play (Spotify)", command=self._spotify_play).grid(row=0, column=1, padx=6)
            ttk.Button(sp_frame, text="Pause (Spotify)", command=self._spotify_pause).grid(row=0, column=2, padx=6)

    def _deck_panel(self, parent, deck):
        box = ttk.LabelFrame(parent, text=deck.name, padding=6)
        box.pack(fill="both", expand=True)
        deck.lbl = ttk.Label(box, text="(no file)")
        deck.lbl.pack(anchor="w")
        btn_frame = ttk.Frame(box)
        btn_frame.pack(fill="x", pady=4)
        ttk.Button(btn_frame, text="Load", command=lambda d=deck: self._load_file(d)).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Play", command=lambda d=deck: self._play(d)).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Pause", command=lambda d=deck: self._pause_unpause(d)).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Stop", command=lambda d=deck: d.stop()).pack(side="left", padx=2)
        vol_frame = ttk.Frame(box)
        vol_frame.pack(fill="x", pady=4)
        ttk.Label(vol_frame, text="Volume").pack(side="left")
        deck.vol_var = tk.DoubleVar(value=1.0)
        ttk.Scale(vol_frame, from_=0.0, to=1.0, orient="horizontal", variable=deck.vol_var,
                  command=lambda v, d=deck: d.set_volume(float(v))).pack(fill="x", expand=True, side="left", padx=6)

    def _load_file(self, deck):
        path = filedialog.askopenfilename(title=f"Load {deck.name}",
                                          filetypes=[("Audio files", "*.wav *.mp3 *.ogg *.flac"), ("All files", "*.*")])
        if not path:
            return
        try:
            deck.load(path)
            deck.lbl.config(text=os.path.basename(path))
        except Exception as e:
            messagebox.showerror("Load error", str(e))

    def _play(self, deck):
        threading.Thread(target=deck.play, daemon=True).start()

    def _pause_unpause(self, deck):
        if deck.paused:
            deck.unpause()
        else:
            deck.pause()

    def _on_cross(self, val):
        x = float(self.cross_var.get())
        a_gain, b_gain = equal_power_crossfade(x)
        self.deck_a.set_volume(a_gain * self.deck_a.vol)
        self.deck_b.set_volume(b_gain * self.deck_b.vol)

    # Spotify handlers
    def _spotify_play(self):
        uri = self.sp_uri.get().strip()
        if not uri:
            messagebox.showinfo("Spotify", "Escriu la URI (spotify:track:...)")
            return
        code, text = self.spotify.play_track(uri)
        if code >= 400:
            messagebox.showerror("Spotify error", f"{code}: {text}")

    def _spotify_pause(self):
        code, text = self.spotify.pause()
        if code >= 400:
            messagebox.showerror("Spotify error", f"{code}: {text}")

    def _update_loop(self):
        # lloc per actualitzar visualitzacions / metadades / VU meters
        self.root.after(200, self._update_loop)

