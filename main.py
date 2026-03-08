import flet as ft
from core.organizer import FileOrganizer
from core.monitor import Sentinel

def main(page: ft.Page):
    # --- CONFIGURACIÓN DE PÁGINA ---
    page.title = "J.A.R.V.I.S. OS"
    page.window_bgcolor = "#050a0f"
    page.window_width = 400
    page.window_height = 550
    page.window_resizable = False
    
    organizer = FileOrganizer()
    log_column = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=200)

    # Función robusta para actualizar la UI desde hilos externos
    def add_log(message):
        print(f"Intentando actualizar UI con: {message}") # Debug extra
        log_column.controls.insert(0, ft.Text(f"> {message}", color="#00ffcc", size=12, font_family="monospace"))
        # IMPORTANTE: En versiones nuevas de Flet, update() es hilo-seguro
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
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon("shield", color="#00ffcc"),
                    ft.Text("SISTEMA_ACTIVO", color="#00ffcc", weight="bold")
                ], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Divider(color="#00ffcc", thickness=1),
                ft.Text("JARVIS: AGENTE DE DESCARGAS", size=22, weight="black", text_align="center", color="white"),
                
                ft.FilledButton(
                    "ORDENAR AHORA",
                    on_click=on_manual_click,
                    style=ft.ButtonStyle(
                        color="black",
                        bgcolor="#00ffcc",
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),
                    width=400
                ),
                
                ft.Text("REPORTE DE MISIÓN:", size=14, color="gray", weight="bold"),
                
                ft.Container(
                    content=log_column,
                    padding=10,
                    border=ft.Border.all(1, "#1a2a3a"),
                    bgcolor="#0a141e",
                    expand=True
                ),
                
                ft.Text("v1.5 - PROTOCOLO CENTINELA ACTIVADO", size=10, color="#1a2a3a")
            ]),
            padding=20,
            expand=True
        )
    )

if __name__ == "__main__":
    # Asegúrate de usar ft.app(main) aquí abajo
    ft.app(main)
