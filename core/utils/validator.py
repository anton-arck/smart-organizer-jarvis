import os
import time

class FileValidator:
    @staticmethod
    def is_stable(file_path: str, required_stability: int = 3) -> bool:
        """
        Verifica si un archivo ha dejado de crecer. 
        Optimizado para que el JIT de Python 3.13 maneje el bucle de espera.
        """
        if not os.path.exists(file_path): 
            return False
            
        last_size = -1
        stable_count = 0
        
        # Aumentamos a 60 intentos (1 minuto de espera para descargas lentas)
        for _ in range(60): 
            try:
                current_size = os.path.getsize(file_path)
                
                if current_size > 0 and current_size == last_size:
                    stable_count += 1
                else:
                    last_size = current_size
                    stable_count = 0
                
                # Si el tamaño se mantiene igual por X segundos, está listo
                if stable_count >= required_stability:
                    return True
            except OSError: 
                return False
                
            time.sleep(1)
        return False
