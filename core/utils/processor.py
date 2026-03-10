import time
import os

class EventProcessor:
    def __init__(self, organizer, callback, network, validator, speak_func, on_success_callback=None):
        self.organizer = organizer
        self.callback = callback
        self.network = network
        self.validator = validator
        self.speak = speak_func
        # Nueva dependencia para los contadores
        self.on_success_callback = on_success_callback

    def process_new_file(self, file_path):
        """Toda la lógica de blindaje centralizada aquí."""
        
        if not self.network.is_connected():
            self.callback("ALERTA: Red inestable. Pausando procesos...", type="system")
            self.speak("Jefe, detecto una caída de red. El archivo quedará en espera.")

        if self.validator.is_stable(file_path):
            network_was_down = False
            if not self.network.is_connected():
                network_was_down = True
                for _ in range(30):
                    if self.network.is_connected():
                        self.callback("SISTEMA: Conexión recuperada. Reanudando...", type="system")
                        break
                    time.sleep(1)

            if self.network.is_connected():
                ext = os.path.splitext(file_path)[1].lower()
                mapping = {
                    '.wav': 'music', '.mp3': 'music', '.flac': 'music',
                    '.py': 'code', '.js': 'code', '.sh': 'code',
                    '.pdf': 'docs', '.docx': 'docs', '.txt': 'docs',
                    '.png': 'image', '.jpg': 'image'
                }
                log_type = mapping.get(ext, "system")

                if self.organizer.move_specific_file(file_path):
                    filename = os.path.basename(file_path)
                    status_msg = f"'{filename}' organizado tras recuperación." if network_was_down else f"'{filename}' organizado."
                    self.callback(status_msg, type=log_type)
                    
                    # --- DISPARADOR DE ANIMACIÓN ---
                    if self.on_success_callback:
                        # Mapeamos al contador correspondiente
                        target = log_type if log_type in ["music", "code"] else "system"
                        self.on_success_callback(target)
                    
                    self.speak(f"Protocolo finalizado. El archivo {filename} ha sido asegurado.")
            else:
                self.callback("ERROR: Tiempo de espera agotado.", type="system")
                self.speak("Jefe, el tiempo de espera de red ha expirado.")
