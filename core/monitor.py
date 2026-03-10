import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from core.utils.network import NetworkChecker
from core.utils.validator import FileValidator
from core.utils.processor import EventProcessor # Nuevo import

class DownloadHandler(FileSystemEventHandler):
    def __init__(self, organizer, callback,animate_func):
        self.organizer = organizer
        self.callback = callback
        self.model_path = "models/friday.onnx"
        
        # Inicializamos herramientas y el Procesador
        self.network = NetworkChecker()
        self.validator = FileValidator()
        self.processor = EventProcessor(
            organizer, callback, self.network, self.validator, self.speak,
            on_success_callback=animate_func
        )

    def speak(self, text):
        """Motor de voz Piper-TTS."""
        abs_model = os.path.abspath(self.model_path)
        temp_wav = os.path.abspath("models/temp_voice.wav")
        if os.path.exists(abs_model):
            try:
                process = subprocess.Popen(
                    ['piper-tts', '--model', abs_model, '--length_scale', '1.2', '--output_file', temp_wav],
                    stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True
                )
                process.communicate(input=text)
                if os.path.exists(temp_wav):
                    subprocess.Popen(['pw-play', temp_wav], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"[!] Error de voz: {e}")

    def on_created(self, event):
        if event.is_directory: return
        # ¡Mira qué limpio queda! Solo llamamos al procesador
        self.processor.process_new_file(event.src_path)

class Sentinel:
    def __init__(self, organizer, callback,animate_func):
        self.observer = Observer()
        self.handler = DownloadHandler(organizer, callback,animate_func)
        self.path = organizer.watch_path

    def start(self):
        self.observer.schedule(self.handler, str(self.path), recursive=False)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
