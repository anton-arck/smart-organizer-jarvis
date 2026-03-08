import flet as ft
from core.organizer import FileOrganizer
from core.monitor import Sentinel

def main(page: ft.Page):
    page.title = "J.A.R.V.I.S. OS"
    page.bgcolor = "#050a0f"  # Color sólido para evitar parpadeos en Wayland
    page.theme_mode = ft.ThemeMode.DARK
    
    # Ajustes de ventana para Tiling Managers
    page.window_width = 400
    page.window_height = 550
    
    organizer = FileOrganizer()
    # Usamos expand=True para que el log ocupe el espacio disponible en el tile
    log_column = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    def add_log(message):
        log_column.controls.insert(
            0, 
            ft.Text(f"> {message}", color="#00ffcc", size=12, font_family="monospace")
        )
        page.update()

    # --- ACTIVACIÓN DEL CENTINELA ---
    sentinel = Sentinel(organizer, add_log)
    sentinel.start()

    # Mover esto AQUÍ ADENTRO soluciona el NameError
    page.on_close = lambda _: sentinel.stop()

    def on_manual_click(e):
        count = organizer.organize()
        add_log(f"MANUAL: {count} archivos organizados.")

    # --- INTERFAZ ---
    
    page.add(
        ft.Text("J.A.R.V.I.S. | MODO WEB", size=25, color="#00ffcc", weight="bold"),
        ft.FilledButton(
            "ORGANIZAR AHORA", 
            on_click=on_manual_click,
            style=ft.ButtonStyle(bgcolor="#00ffcc", color="black")
        ),
        ft.Container(
            content=log_column,
            height=400, # Altura fija para asegurar visibilidad en web
            border=ft.Border.all(1, "#1a2a3a"),
            bgcolor="#0a141e",
            padding=10,
            border_radius=5
        )
    )

if __name__ == "__main__":
    # 'view' puede ser ft.AppView.WEB_BROWSER para abrir el navegador por defecto
    # 'port' te permite elegir en qué puerto de tu localhost correrá Jarvis
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)
