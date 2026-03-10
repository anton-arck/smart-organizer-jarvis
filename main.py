import flet as ft
from core.organizer import FileOrganizer
from core.monitor import Sentinel
from ui.components import DashboardUI # Importamos la UI modular
import threading
import asyncio
import time

async def main(page: ft.Page):
    # Guardamos el loop actual para que el monitor pueda encontrarlo
    main_loop = asyncio.get_running_loop()
    
    # --- CONFIGURACIÓN UI ---
    page.title = "F.R.I.D.A.Y. OS | Core"
    page.bgcolor = "#050a0f"
    page.window_width = 420
    page.window_height = 650
    
    # Instanciamos la UI modular
    dashboard = DashboardUI()
    log_column = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    async def add_log(message, type="system"):
        colors = {
            "system": "#00ffcc", 
            "music": "#ff00ff", 
            "code": "#00ff00", 
            "manual": "#ffcc00"
        }
        new_log = ft.Text(
            f"> [{type.upper()}] {message}", 
            color=colors.get(type, "#ffffff"), 
            size=13, 
            font_family="monospace"
        )
        log_column.controls.insert(0, new_log)
        page.update()

    # --- PUENTES ASÍNCRONOS ---
    def sync_add_log(msg, type="system"):
        main_loop.call_soon_threadsafe(
            lambda: asyncio.create_task(add_log(msg, type))
        )

    def sync_animate(type_key):
        """Puente para disparar la animación de las Cards."""
        main_loop.call_soon_threadsafe(
            lambda: asyncio.create_task(dashboard.animate_count(type_key, page))
        )

    # --- INICIALIZACIÓN ---
    organizer = FileOrganizer()
    sentinel = Sentinel(organizer, sync_add_log, sync_animate)
    sentinel.start()

    # --- FUNCIÓN DE BIENVENIDA ---
    def delayed_greeting():
        """Espera a que el sistema cargue y lanza el saludo inicial."""
        time.sleep(1.5)
        saludo = "Sistemas de monitoreo activos. Su laptop está optimizada para empezar este día."
        # Accedemos al motor de voz a través del handler del sentinel
        sentinel.handler.speak(saludo)

    # Lanzamos el saludo en un hilo separado para no bloquear la UI
    threading.Thread(target=delayed_greeting, daemon=True).start()

    # --- ENSAMBLAJE DE PANTALLA ---
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("F.R.I.D.A.Y. | DASHBOARD", size=22, color="#00ffcc", weight="bold"),
                dashboard.build_dashboard(), # Insertamos el dashboard modular
                ft.Divider(height=10, color="#1a2a3a"),
                ft.FilledButton(
                    "ORGANIZAR AHORA", 
                    on_click=lambda _: asyncio.create_task(add_log("Manual trigger...", "manual")), 
                    width=400,
                    style=ft.ButtonStyle(bgcolor="#1a2a3a", color="#00ffcc")
                ),
                ft.Container(
                    content=log_column, 
                    expand=True, 
                    bgcolor="#0a141e", 
                    padding=10, 
                    border_radius=5
                )
            ], spacing=15, expand=True),
            padding=20, 
            expand=True
        )
    )

    # Manejo de cierre limpio
    def handle_close(e):
        sentinel.stop()
        page.window_close()

    page.on_close = handle_close

if __name__ == "__main__":
    ft.run(main)
