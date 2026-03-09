import time
import subprocess
import os
import random # Para las frases variadas
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DownloadHandler(FileSystemEventHandler):
    def __init__(self, organizer, callback):
        self.organizer = organizer
        self.callback = callback
        # ASEGÚRATE de que el nombre coincida con tu archivo en la carpeta models
        self.model_path = "models/friday.onnx" 

    def speak(self, text):
        """Protocolo F.R.I.D.A.Y. - Solución definitiva sin tuberías de shell."""
        abs_model = os.path.abspath(self.model_path)
        temp_wav = os.path.abspath("models/temp_voice.wav")
        
        if os.path.exists(abs_model):
            try:
                # Ejecutamos piper-tts sin usar 'echo' ni '|' de shell
                # Pasamos el texto directamente a través de stdin.write
                process = subprocess.Popen(
                    ['piper-tts', '--model', abs_model,'--length_scale','1.1', '--output_file', temp_wav],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    text=True
                )
                
                # Enviamos el texto y cerramos el pipe de forma segura
                process.communicate(input=text)
                
                # Una vez generado el archivo, reproducimos con Pipewire
                if os.path.exists(temp_wav):
                    subprocess.Popen(
                        ['pw-play', temp_wav],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
            except Exception as e:
                print(f"[!] Error crítico en el protocolo de voz: {e}")
        else:
            print(f"[!] Modelo no encontrado en: {abs_model}")

    def on_created(self, event):
        if event.is_directory: return
        
        time.sleep(2) # Esperar a que la descarga termine
        
        # Detectar qué tipo de archivo entró para elegir el color
        ext = os.path.splitext(event.src_path)[1].lower()
        
        if ext in ['.wav', '.mp3', '.flac']:
            log_type = "music"
        elif ext in ['.py', '.pi', '.js', '.html']:
            log_type = "code"
        elif ext in ['.pdf', '.docx', '.txt', '.xlsx']:
            log_type = "docs"
        elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
            log_type = "image"
        elif ext in ['.mp4', '.mkv', '.mov', '.avi']:
            log_type = "video"
        else:
            log_type = "system"

        count = self.organizer.organize()
        
        if count > 0:
            msg = f"Se han detectado y organizado {count} elementos."
            self.callback(msg, type=log_type)
            
            # Frase para Claude (MX)
            self.speak(f"Jefe, he procesado nuevos archivos de tipo {log_type}.")

  

# ... (Clase Sentinel sigue igual)

class Sentinel:
    def __init__(self, organizer, callback):
        self.observer = Observer()
        # El callback que recibe aquí ya es 'sync_add_log' de main.py
        self.handler = DownloadHandler(organizer, callback)
        self.path = organizer.watch_path

    def start(self):
        self.observer.schedule(self.handler, str(self.path), recursive=False)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
