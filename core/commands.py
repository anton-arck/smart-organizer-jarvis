from abc import ABC, abstractmethod
from pathlib import Path
import shutil

class Command(ABC):
    @abstractmethod
    def execute(self) -> bool:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

class OrganizeFileCommand(Command):
    """Encapsula la acción de organizar un archivo específico."""
    def __init__(self, organizer, file_path: str):
        self.organizer = organizer
        self.file_path = Path(file_path)
        self.dest_path = None
        self.filename = self.file_path.name

    def execute(self) -> bool:
        """Ejecuta el movimiento basado en la categoría detectada."""
        category = self.organizer._get_category(self.file_path.suffix)
        if category:
            dest_dir = self.organizer.watch_path / category
            dest_dir.mkdir(parents=True, exist_ok=True)
            self.dest_path = dest_dir / self.filename
            try:
                # El JIT optimizará estas llamadas del sistema en Python 3.13
                shutil.move(str(self.file_path), str(self.dest_path))
                return True
            except Exception as e:
                print(f"[!] Error en Command Execute: {e}")
        return False

    def undo(self) -> None:
        """Revierte el movimiento si es necesario."""
        if self.dest_path and self.dest_path.exists():
            shutil.move(str(self.dest_path), str(self.file_path))
