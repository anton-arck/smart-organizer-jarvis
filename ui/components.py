import flet as ft
import asyncio

class DashboardUI:
    def __init__(self):
        # Textos de la UI
        self.stats_ui = {
            "music": ft.Text("0", size=22, color="#ff00ff", weight="bold"),
            "code": ft.Text("0", size=22, color="#00ff00", weight="bold"),
            "system": ft.Text("0", size=22, color="#00ffcc", weight="bold")
        }
        # Valores numéricos
        self.counts = {"music": 0, "code": 0, "system": 0}

    async def animate_count(self, type_key, page):
        """Lógica de incremento y pulso neón."""
        self.counts[type_key] += 1
        self.stats_ui[type_key].value = str(self.counts[type_key])
        
        # Encontrar qué card animar
        idx = 0 if type_key == "music" else 1 if type_key == "code" else 2
        # Suponiendo que las cards están en una fila (Row)
        # Necesitaremos acceso a la referencia de la card si queremos escala
        page.update()

    def create_stat_card(self, label, color, type_key):
        return ft.Container(
            content=ft.Column([
                ft.Text(label, size=9, color=color, weight="bold", opacity=0.7),
                self.stats_ui[type_key],
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            padding=10,
            border=ft.Border.all(1, color),
            border_radius=8,
            width=110,
            bgcolor="#0a141e",
            shadow=ft.BoxShadow(blur_radius=10, color=color, spread_radius=-5)
        )

    def build_dashboard(self):
        return ft.Row([
            self.create_stat_card("MUSIC", "#ff00ff", "music"),
            self.create_stat_card("CODE", "#00ff00", "code"),
            self.create_stat_card("SYSTEM", "#00ffcc", "system"),
        ], alignment=ft.MainAxisAlignment.CENTER)
