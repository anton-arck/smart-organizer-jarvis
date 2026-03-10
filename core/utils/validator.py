import os
import time

class FileValidator:
    @staticmethod
    def is_stable(file_path, required_stability=2): # 2 segundos es suficiente
        if not os.path.exists(file_path): return False
        last_size = -1
        stable_count = 0
        
        for _ in range(20): 
            try:
                current_size = os.path.getsize(file_path)
                # Eliminamos la restricción de 'current_size > 0'
                if current_size == last_size:
                    stable_count += 1
                else:
                    last_size = current_size
                    stable_count = 0
                
                if stable_count >= required_stability:
                    return True
            except OSError: return False
            time.sleep(1)
        return False
