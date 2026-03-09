import flet as ft
from core.organizer import FileOrganizer
from core.monitor import Sentinel
import threading
import asyncio
import os

async def main(page: ft.Page):
    # Guardamos el loop actual para que el monitor pueda encontrarlo
    main_loop = asyncio.get_running_loop()
    
    page.title = "F.R.I.D.A.Y. OS"
    page.bgcolor = "#050a0f"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 550
    
    organizer = FileOrganizer()
    log_column = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    async def add_log(message, type="system"):
        colors = {
            "system": "#00ffcc", "music": "#ff00ff", "code": "#00ff00",
            "docs": "#ffffff", "image": "#0077ff", "video": "#ff4400", "manual": "#ffcc00"
        }
        selected_color = colors.get(type, "#ffffff")
        new_log = ft.Text("", color=selected_color, size=13, font_family="monospace")
        log_column.controls.insert(0, new_log)
        
        full_text = f"> [{type.upper()}] {message}"
        for i in range(len(full_text) + 1):
            new_log.value = full_text[:i]
            page.update()
            await asyncio.sleep(0.01)

    # PUENTE CORREGIDO: Usamos la referencia 'main_loop'
    def sync_add_log(msg, type="system"):
        main_loop.call_soon_threadsafe(
            lambda: asyncio.create_task(add_log(msg, type))
        )

    sentinel = Sentinel(organizer, sync_add_log)
    sentinel.start()

    def delayed_greeting():
        saludo = "Sistemas de monitoreo activos. Su laptop esta optimizada para empezar este dia."
        sentinel.handler.speak(saludo)

    threading.Thread(target=delayed_greeting, daemon=True).start()

    async def on_manual_click(e):
        count = organizer.organize()
        await add_log(f"MANUAL: {count} archivos organizados.", type="manual")

    # Corregido: Usamos handle_close para evitar el AttributeError y errores de GTK
    def handle_close(e):
        sentinel.stop()
        page.window_destroy()

    page.on_close = handle_close

    page.add(
        ft.Text("F.R.I.D.A.Y. | CORE", size=25, color="#00ffcc", weight="bold"),
        ft.FilledButton(
            "ORGANIZAR AHORA", 
            on_click=on_manual_click,
            style=ft.ButtonStyle(bgcolor="#00ffcc", color="black")
        ),
        ft.Container(
            content=log_column,
            expand=True,
            border=ft.Border.all(1, "#1a2a3a"),
            bgcolor="#0a141e",
            padding=10,
            border_radius=5
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
