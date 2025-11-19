import tkinter as tk
from ventanas.gestionar_alumnos import gestionar_alumnos
from ventanas.gestionar_cursos import gestionar_cursos
from ventanas.gestionar_asignaciones import gestionar_asignaciones
from ventanas.gestionar_entregas import gestionar_entregas
from ventanas.gestionar_tareas import gestionar_tareas
from core.estilos_utilidades import COLOR_FONDO, COLOR_TITULO_FONDO, COLOR_TITULO_TEXTO, SALIR_BOTON, SALIR_COLOR_TEXTO, SALIR_HOVER, centrar_ventana, crear_boton

def main():
    # VENTANA PRINCIPAL
    main = tk.Tk()
    main.title("Gestor SQLite")
    main.config(bg=COLOR_FONDO)
    centrar_ventana(main, 400, 250)
    main.resizable(False, False)

    # FRAME TÍTULO
    frame_titulo = tk.Frame(main, bg=COLOR_TITULO_FONDO, height=40)
    frame_titulo.pack(fill="x")
    tk.Label(
        frame_titulo, 
        text="GESTOR SQLITE", 
        font=("Arial", 12, "bold"),
        bg=COLOR_TITULO_FONDO, 
        fg=COLOR_TITULO_TEXTO, 
        pady=10
    ).pack()

    # FRAME BOTONES
    frame_principal = tk.Frame(main, bg=COLOR_FONDO)
    frame_principal.pack(pady=15)

    #################### FILA 0 ####################
    b_alumnos = crear_boton(
        frame_principal, 
        "Gestionar alumnos", 
        lambda: gestionar_alumnos(main), 
        width=18
    )
    b_alumnos.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    b_cursos = crear_boton(
        frame_principal, 
        "Gestionar cursos", 
        lambda: gestionar_cursos(main), 
        width=18
    )
    b_cursos.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    #################### FILA 1 ####################=
    b_asignaciones = crear_boton(
        frame_principal, 
        "Gestionar cursos de alumnos", 
        lambda: gestionar_asignaciones(main), 
        width=40
    )
    b_asignaciones.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

    #################### FILA 2 ####################
    b_entregas = crear_boton(
        frame_principal, 
        "Gestionar entregas", 
        lambda: gestionar_entregas(main), 
        width=18
    )
    b_entregas.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    b_tareas = crear_boton(
        frame_principal, 
        "Gestionar tareas", 
        lambda: gestionar_tareas(main), 
        width=18
    )
    b_tareas.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    #################### FILA 3 ####################
    b_salir = crear_boton(
        frame_principal, 
        "Salir", 
        main.quit,
        bg=SALIR_BOTON, 
        fg=SALIR_COLOR_TEXTO, 
        hover_bg=SALIR_HOVER
    )
    b_salir.grid(row=3, column=0, columnspan=2, pady=15, sticky="ew", padx=5)

    # BUCLE VENTANA
    main.mainloop()


# __main__
if __name__ == "__main__":
    main()