import threading
import pyttsx3

class VoiceAlertManager:
    def __init__(self):
        self.enabled = True
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)
        self.lock = threading.Lock()

    def speak(self, text):
        if not self.enabled:
            return
        def _speak():
            with self.lock:
                self.engine.say(text)
                self.engine.runAndWait()
        threading.Thread(target=_speak, daemon=True).start()

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled