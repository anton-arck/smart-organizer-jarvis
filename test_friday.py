import os
import time
import subprocess
from pathlib import Path

def toggle_internet(status):
    """Usa comandos de sistema para simular caída de red."""
    if status == "off":
        print("\n🌐 [SUDO] Bloqueando acceso a 8.8.8.8 (Simulando caída)...")
        subprocess.run(["sudo", "ip", "route", "add", "blackhole", "8.8.8.8"])
    else:
        print("\n🌐 [SUDO] Restaurando acceso a 8.8.8.8 (Red recuperada)...")
        subprocess.run(["sudo", "ip", "route", "del", "blackhole", "8.8.8.8"])

def run_suite():
    download_path = Path.home() / "Downloads"
    test_file = download_path / "test_hacker.wav"
    
    print("🚀 INICIANDO SUITE DE PRUEBAS: PROTOCOLO DE RED Y ARCHIVO")
    
    try:
        with open(test_file, "wb") as f:
            for i in range(1, 11):
                # Escribimos datos
                f.write(os.urandom(512 * 1024)) # 512KB
                f.flush()
                os.fsync(f.fileno())
                print(f"📦 Escribiendo bloque {i}/10...")

                # --- SIMULACIÓN DE RED ---
                if i == 4:
                    toggle_internet("off")
                    print("⚠️ Claude debería avisar sobre la inestabilidad ahora.")
                
                if i == 8:
                    print("⏳ Manteniendo red caída para probar la paciencia de F.R.I.D.A.Y...")
                    time.sleep(5)
                    toggle_internet("on")
                
                time.sleep(2)

        print("\n✅ Escritura finalizada. Esperando procesamiento final...")
        
    except Exception as e:
        print(f"❌ Error en el test: {e}")
    finally:
        # Aseguramos que la red se restaure incluso si el script falla
        subprocess.run(["sudo", "ip", "route", "del", "blackhole", "8.8.8.8"], 
                       stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    run_suite()
