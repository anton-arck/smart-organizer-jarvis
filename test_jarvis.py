import unittest
import os
import shutil
from pathlib import Path
from core.organizer import FileOrganizer

class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        """Configuración antes de cada prueba: crea una carpeta de prueba temporal."""
        self.test_dir = Path("./test_workspace")
        self.test_dir.mkdir(exist_ok=True)
        self.organizer = FileOrganizer()
        # Redirigimos la ruta de vigilancia a nuestra carpeta de test
        self.organizer.watch_path = self.test_dir

    def tearDown(self):
        """Limpieza después de cada prueba: borra la carpeta temporal."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_create_category_folder(self):
        """Prueba si Jarvis crea la carpeta cuando no existe."""
        test_file = self.test_dir / "documento.pdf"
        test_file.touch() # Crea un archivo vacío
        
        self.organizer.organize()
        
        pdf_folder = self.test_dir / "PDFs"
        self.assertTrue(pdf_folder.exists(), "La carpeta PDFs debería haber sido creada.")
        self.assertTrue((pdf_folder / "documento.pdf").exists(), "El archivo debería haberse movido.")

    def test_multiple_categories(self):
        """Prueba la organización de múltiples tipos de archivos a la vez."""
        (self.test_dir / "imagen.png").touch()
        (self.test_dir / "script.py").touch()
        (self.test_dir / "desconocido.xyz").touch()

        count = self.organizer.organize()
        
        self.assertEqual(count, 2, "Debería haber movido exactamente 2 archivos.")
        self.assertTrue((self.test_dir / "Imagenes/imagen.png").exists())
        self.assertTrue((self.test_dir / "Scripts/script.py").exists())
        self.assertTrue((self.test_dir / "desconocido.xyz").exists(), "El archivo desconocido no debe moverse.")

if __name__ == "__main__":
    unittest.main()
