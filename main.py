import flet as ft
from core.organizer import FileOrganizer
from core.monitor import Sentinel
from ui.components import DashboardUI
import asyncio

async def main(page: ft.Page):
    main_loop = asyncio.get_running_loop()
    
    # --- CONFIGURACIÓN UI ---
    page.title = "F.R.I.D.A.Y. OS | Core"
    page.bgcolor = "#050a0f"
    page.window_width = 420
    page.window_height = 650
    page.theme_mode = ft.ThemeMode.DARK
    
    dashboard = DashboardUI()
    log_column = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    async def add_log(message, type="system"):
        colors = {"system": "#00ffcc", "music": "#ff00ff", "code": "#00ff00", "manual": "#ffcc00"}
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
        main_loop.call_soon_threadsafe(lambda: asyncio.create_task(add_log(msg, type)))

    def sync_animate(type_key):
        main_loop.call_soon_threadsafe(lambda: asyncio.create_task(dashboard.animate_count(type_key, page)))

    # --- INICIALIZACIÓN ---
    organizer = FileOrganizer()
    sentinel = Sentinel(organizer, sync_add_log, sync_animate)
    sentinel.start()

    # --- LÓGICA DEL BOTÓN (CORREGIDA) ---
    async def handle_manual_organize(e):
        await add_log("Iniciando limpieza manual...", "manual")
        # El método organize() devuelve la cantidad de archivos movidos
        count = organizer.organize() 
        
        if count > 0:
            await add_log(f"Éxito: {count} archivos organizados.", "system")
            sentinel.handler.speak(f"Limpieza completada, jefe. He movido {count} archivos.")
            # Actualizamos el contador general de la UI
            await dashboard.animate_count("system", page)
        else:
            await add_log("Nada que organizar por ahora.", "system")
            sentinel.handler.speak("La carpeta ya está limpia.")

    # --- SALUDO ASÍNCRONO ---
    async def delayed_greeting():
        await asyncio.sleep(2)
        sentinel.handler.speak("Sistemas de monitoreo activos. Laptop optimizada, jefe.")

    asyncio.create_task(delayed_greeting())

    # --- ENSAMBLAJE ---
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("F.R.I.D.A.Y. | DASHBOARD", size=22, color="#00ffcc", weight="bold"),
                dashboard.build_dashboard(),
                ft.Divider(height=10, color="#1a2a3a"),
                ft.FilledButton(
                    "ORGANIZAR AHORA", 
                    on_click=handle_manual_organize, # <--- Ahora llama a la función corregida
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

    page.on_close = lambda _: sentinel.stop()

if __name__ == "__main__":
    ft.run(main)
