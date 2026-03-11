import os
import time
from pathlib import Path

def simular_descarga_pesada(nombre_archivo: str, pasos: int = 10, delay: int = 2):
    """
    Simula la descarga de un archivo grande que crece con el tiempo.
    Esto disparará la lógica de is_stable() en el validador.
    """
    descargas = Path.home() / "Downloads"
    ruta_test = descargas / nombre_archivo
    
    print(f"[*] Iniciando descarga simulada en: {ruta_test}")
    
    try:
        with open(ruta_test, "wb") as f:
            for i in range(pasos):
                # Escribimos 1MB de datos basura en cada paso
                f.write(os.urandom(1024 * 1024))
                f.flush()
                os.fsync(f.fileno()) # Forzamos escritura en disco para el SO
                
                print(f"[!] Descargando: {i+1}/{pasos} MB...")
                time.sleep(delay)
                
        print(f"[OK] Descarga de '{nombre_archivo}' completada.")
    except Exception as e:
        print(f"[X] Error en simulación: {e}")

if __name__ == "__main__":
    # Prueba con un archivo de música para ver si F.R.I.D.A.Y. lo mueve al terminar
    simular_descarga_pesada("set_techno_2026.mp3", pasos=5, delay=3)
