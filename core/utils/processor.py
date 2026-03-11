import time
import os
from core.commands import OrganizeFileCommand

class EventProcessor:
    def __init__(self, organizer, callback, network, validator, speak_func, on_success_callback=None):
        self.organizer = organizer
        self.callback = callback
        self.network = network
        self.validator = validator
        self.speak = speak_func
        self.on_success_callback = on_success_callback

    def process_new_file(self, file_path: str):
        """Procesa un archivo aplicando blindaje de red y validación de estabilidad."""
        
        if not self.network.is_connected():
            self.callback("ALERTA: Red inestable. Pausando procesos...", type="system")
            self.speak("Jefe, detecto una caída de red.")

        if self.validator.is_stable(file_path):
            if not self._wait_for_network():
                self.callback("ERROR: Tiempo de espera de red agotado.", type="system")
                self.speak("El tiempo de espera ha expirado.")
                return

            # Uso del Patrón Command para organizar
            cmd = OrganizeFileCommand(self.organizer, file_path)
            
            if cmd.execute():
                log_type = self._get_log_type(cmd.file_path.suffix.lower())
                self.callback(f"'{cmd.filename}' organizado con éxito.", type=log_type)
                
                if self.on_success_callback:
                    # Mapeo a las categorías de la UI (Music, Code o System)
                    target = log_type if log_type in ["music", "code"] else "system"
                    self.on_success_callback(target)
                
                self.speak(f"Protocolo finalizado. El archivo {cmd.filename} ha sido asegurado.")

    def _wait_for_network(self) -> bool:
        """Bucle de espera optimizado para el JIT."""
        if self.network.is_connected():
            return True
        for _ in range(30):
            if self.network.is_connected():
                self.callback("SISTEMA: Conexión recuperada.", type="system")
                return True
            time.sleep(1)
        return False

    def _get_log_type(self, ext: str) -> str:
        """Mapeo de extensiones a tipos de log de la UI."""
        mapping = {
            '.wav': 'music', '.mp3': 'music', '.flac': 'music', '.ogg': 'music',
            '.py': 'code', '.js': 'code', '.sh': 'code', '.fish': 'code',
            '.pdf': 'docs', '.docx': 'docs', '.txt': 'docs',
            '.png': 'image', '.jpg': 'image'
        }
        return mapping.get(ext, "system")
