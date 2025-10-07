# core/audio_utils.py
# petits helpers relacionats amb l'audio (crossfade curves, equal-power, etc.)
import math

def equal_power_crossfade(x: float) -> tuple:
    """
    x: 0.0 .. 1.0
    retorna (gainA, gainB) amb corba equal-power
    """
    x = max(0.0, min(1.0, float(x)))
    a = math.cos(x * math.pi / 2)
    b = math.cos((1.0 - x) * math.pi / 2)
    # Normalize so max is 1.0 (optional)
    return a, b

