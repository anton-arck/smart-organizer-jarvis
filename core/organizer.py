import os
import shutil
from pathlib import Path

class FileOrganizer:
    def __init__(self):
        # Localiza la carpeta de Descargas del usuario actual de forma automática
        self.watch_path = Path.home() / "Downloads"
        
        # Diccionario de categorías (puedes ampliarlo luego)
        self.categories = {
            "PDFs": [".pdf"],
            "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
            "Documentos_Office": [".docx", ".xlsx", ".pptx"],
            "Scripts": [".py", ".js", ".sh", ".fish"],
            "Comprimidos": [".zip", ".rar", ".7z"]
        }

    def _get_category(self, extension):
        for category, extensions in self.categories.items():
            if extension.lower() in extensions:
                return category
        return None # No mover archivos desconocidos por ahora

    def organize(self):
        if not self.watch_path.exists():
            return 0, "Error: No se encontró la carpeta Downloads."

        moved_count = 0
        
        for item in self.watch_path.iterdir():
            # Solo procesar archivos, ignorar carpetas y archivos ocultos
            if item.is_file() and not item.name.startswith('.'):
                category = self._get_category(item.suffix)
                
                if category:
                    dest_dir = self.watch_path / category
                    
                    # SI NO EXISTE LA CARPETA, JARVIS LA CREA
                    if not dest_dir.exists():
                        dest_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Mover el archivo
                    try:
                        shutil.move(str(item), str(dest_dir / item.name))
                        moved_count += 1
                    except Exception as e:
                        print(f"Error al mover {item.name}: {e}")
        
        return moved_count
