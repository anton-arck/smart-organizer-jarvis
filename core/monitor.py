import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DownloadHandler(FileSystemEventHandler):
    def __init__(self, organizer, callback):
        self.organizer = organizer
        self.callback = callback

    def on_created(self, event):
        # Ignoramos si es una carpeta
        if event.is_directory:
            return
        
        # Pequeña pausa para asegurar que el archivo terminó de descargarse
        time.sleep(2)
        
        # Ejecutamos la organización
        count = self.organizer.organize()
        
        if count > 0:
            # Enviamos el mensaje de vuelta a la interfaz de Flet
            #self.callback(f"CENTINELA: {count} archivo(s) detectado(s).")
            msg = f"CENTINELA: {count} archivo(s) procesado(s)."
            print(f"[DEBUG] {msg}") # Esto saldrá en tu terminal de Cusco
            self.callback(msg)

class Sentinel:
    """Esta es la clase que main.py no encontraba."""
    def __init__(self, organizer, callback):
        self.observer = Observer()
        self.handler = DownloadHandler(organizer, callback)
        self.path = organizer.watch_path

    def start(self):
        # Configuramos el observador para mirar la carpeta de Descargas
        self.observer.schedule(self.handler, str(self.path), recursive=False)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
