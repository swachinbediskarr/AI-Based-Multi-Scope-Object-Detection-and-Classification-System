import threading
import time
import pyttsx3

from config import (
    VOICE_ALERT_ENABLED,
    ALERT_COOLDOWN
)

class AlertManager:
    def __init__(self):

        self.voice_enabled = (
            VOICE_ALERT_ENABLED
        )

        self.alert_cooldown = (
            ALERT_COOLDOWN
        )

        self.last_alert_times = {}

        self.voice_lock = (
            threading.Lock()
        )

        self.engine = (
            pyttsx3.init()
        )

        self.engine.setProperty(
            "rate",
            160
        )

        print(
            "[ALERT] Alert Manager initialized."
        )
    def toggle_voice(self):
        self.voice_enabled = (
            not self.voice_enabled
        )
        return self.voice_enabled
    def can_alert(
        self,
        track_id
    ):
        current_time = time.time()

        last_time = (
            self.last_alert_times.get(
                track_id,
                0
            )
        )
        if (
            current_time - last_time
            >=
            self.alert_cooldown
        ):
            self.last_alert_times[
                track_id
            ] = current_time
            return True
        return False

    def speak(
        self,
        message
    ):
        if not self.voice_enabled:
            return
        thread = threading.Thread(
            target=self._speak_thread,
            args=(message,),
            daemon=True
        )

        thread.start()

    def _speak_thread(
        self,
        message
    ):
        with self.voice_lock:

            self.engine.say(
                message
            )
            self.engine.runAndWait()