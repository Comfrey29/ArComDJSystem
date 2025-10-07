# controllers/midi_controller.py
import threading

try:
    import mido
except Exception:
    mido = None

class MIDIController:
    """
    Descobreix ports MIDI i escolta missatges en background.
    Callback signature: fn(message: mido.Message)
    """
    def __init__(self, preferred_input=None):
        self.inport = None
        self.thread = None
        self.running = False
        self.preferred_input = preferred_input
        if mido:
            names = mido.get_input_names()
            if not names:
                print("[MIDI] No MIDI input ports found.")
            else:
                name = preferred_input or names[0]
                try:
                    self.inport = mido.open_input(name)
                    print(f"[MIDI] Opened input: {name}")
                except Exception as e:
                    print(f"[MIDI] Cannot open MIDI input {name}: {e}")

    def start_listening(self, callback):
        if not self.inport:
            print("[MIDI] No input to listen to.")
            return
        if self.running:
            return
        self.running = True
        def _loop():
            for msg in self.inport:
                if not self.running:
                    break
                try:
                    callback(msg)
                except Exception as e:
                    print("[MIDI] callback error:", e)
        self.thread = threading.Thread(target=_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        try:
            if self.inport:
                self.inport.close()
        except Exception:
            pass

