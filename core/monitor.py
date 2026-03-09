import time
import subprocess
import os
import socket
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DownloadHandler(FileSystemEventHandler):
    def __init__(self, organizer, callback):
        self.organizer = organizer
        self.callback = callback
        self.model_path = "models/friday.onnx" 

    def is_connected(self):
        """Verifica si hay conexión a internet activa (Detección de parpadeos)."""
        try:
            # Intentamos conectar al DNS de Google (ligero y rápido)
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def wait_for_file_ready(self, file_path):
        """Protocolo F.R.I.D.A.Y.: Verificación cruzada Tamaño + Internet."""
        last_size = -1
        stable_count = 0
        required_stability = 4 # Segundos de estabilidad requeridos
        
        while True:
            if not os.path.exists(file_path):
                return False
                
            try:
                current_size = os.path.getsize(file_path)
            except OSError:
                time.sleep(1)
                continue

            # CASO A: El archivo sigue creciendo
            if current_size > last_size:
                last_size = current_size
                stable_count = 0
            
            # CASO B: El tamaño se estancó
            elif current_size == last_size and current_size > 0:
                if self.is_connected():
                    stable_count += 1
                    # Si hay internet y el tamaño es estable, la descarga terminó
                    if stable_count >= required_stability:
                        try:
                            # Verificación final de bloqueo del sistema
                            with open(file_path, 'a'):
                                return True 
                        except IOError:
                            stable_count = 0 
                else:
                    # Alerta de red: pausamos y avisamos solo una vez
                    if stable_count == 0:
                        self.speak("Señor, detecto inestabilidad en la red. Pausando organización.")
                    stable_count = -1 
                    time.sleep(4) # Espera larga para reintento de red

            last_size = current_size
            time.sleep(1)

    def speak(self, text):
        """Protocolo de voz neuronal Claude (MX)."""
        abs_model = os.path.abspath(self.model_path)
        temp_wav = os.path.abspath("models/temp_voice.wav")
        
        if os.path.exists(abs_model):
            try:
                process = subprocess.Popen(
                    ['piper-tts', '--model', abs_model,'--length_scale','1.2', '--output_file', temp_wav],
                    stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True
                )
                process.communicate(input=text)
                if os.path.exists(temp_wav):
                    subprocess.Popen(['pw-play', temp_wav], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"[!] Error en protocolo de voz: {e}")

    def on_created(self, event):
        if event.is_directory: return
        
        # Iniciamos el nuevo protocolo de espera inteligente
        if self.wait_for_file_ready(event.src_path):
            ext = os.path.splitext(event.src_path)[1].lower()
            
            # Mapeo de tipos para la interfaz Cyberpunk
            if ext in ['.wav', '.mp3', '.flac']: log_type = "music"
            elif ext in ['.py', '.pi', '.js', '.html']: log_type = "code"
            elif ext in ['.pdf', '.docx', '.txt', '.xlsx']: log_type = "docs"
            elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg']: log_type = "image"
            elif ext in ['.mp4', '.mkv', '.mov', '.avi']: log_type = "video"
            else: log_type = "system"

            count = self.organizer.organize()
            
            if count > 0:
                msg = f"Protocolo completado: {count} elementos procesados."
                self.callback(msg, type=log_type)
                self.speak(f"Jefe, he procesado nuevos archivos de tipo {log_type}.")

class Sentinel:
    def __init__(self, organizer, callback):
        self.observer = Observer()
        self.handler = DownloadHandler(organizer, callback)
        self.path = organizer.watch_path

    def start(self):
        self.observer.schedule(self.handler, str(self.path), recursive=False)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
