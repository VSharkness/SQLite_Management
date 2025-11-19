import tkinter as tk
from tkinter import messagebox
from core.estilos_utilidades import COLOR_FONDO, COLOR_LABEL, COLOR_ERROR, crear_boton, centrar_ventana
from core.widgets import TooltipTreeview, AutocompleteCombobox
from core.treeview_utilidades import treeview
from funciones import (
    obtener_alumnos, obtener_alumnos_curso, obtener_cursos, asignar_alumno_curso, eliminar_alumno_curso
)

def gestionar_asignaciones(main):

    # CONFIGURACIÓN VENTANA
    ventana = tk.Toplevel(main)
    ventana.title("Inscribir alumnos a cursos")
    ventana.config(bg=COLOR_FONDO)
    centrar_ventana(ventana, 500, 430)
    ventana.resizable(False, False)
    ventana.columnconfigure(1, weight=1)

#FILA 0 - LABEL Y COMBO ALUMNO
    tk.Label(ventana, text="Alumno:", bg=COLOR_FONDO, fg=COLOR_LABEL).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    combo_alumno = AutocompleteCombobox(ventana, state="normal")
    combo_alumno.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    combo_alumno.set_completion_list([f"{a[0]} ({a[1]})" for a in obtener_alumnos()])

#FILA 1 - LABEL Y COMBO CURSO
    tk.Label(ventana, text="Curso:", bg=COLOR_FONDO, fg=COLOR_LABEL).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    combo_curso = AutocompleteCombobox(ventana, state="normal")
    combo_curso.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    combo_curso.set_completion_list([f"{c[0]} ({c[1]})" for c in obtener_cursos()])

#FILA 2 - LABEL DE ERROR
    error_label = tk.Label(ventana, text="", fg=COLOR_ERROR, bg=COLOR_FONDO)
    error_label.grid(row=2, column=0, columnspan=2)

#FILA 3 - BOTONES FUNCIONALES
    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

    # FUNCIÓN BOTÓN INSCRIBIR
    def asignar():
        id_alumno = combo_alumno.get_id()
        id_curso = combo_curso.get_id()
        if not id_alumno or not id_curso:
            error_label.config(text="Selecciona un alumno y un curso válidos")
            return
        try:
            asignar_alumno_curso(id_alumno, id_curso)
            combo_alumno.reset()
            combo_curso.reset()
            error_label.config(text="")
            actualizar_tabla()
        except ValueError as e:
            error_label.config(text=str(e))
            combo_alumno.set("")
            combo_curso.set("")

    boton_asignar = crear_boton(frame_botones, "Inscribir", asignar)
    boton_asignar.grid(row=0, column=0, padx=5, ipadx=5, ipady=3, sticky="ew")

    # FUNCIÓN BOTÓN BORRAR
    def borrar_seleccionado():
        selected = tabla.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona una inscripción", parent=ventana)
            return
        for item in selected:
            try:
                id_alumno, id_curso = map(int, item.split("-"))
                eliminar_alumno_curso(id_alumno, id_curso)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo borrar la inscripción:\n{e}", parent=ventana)
        actualizar_tabla()

    b_borrar = crear_boton(frame_botones, "Borrar inscripción", borrar_seleccionado)
    b_borrar.grid(row=0, column=1, padx=5, ipadx=5, ipady=3, sticky="ew")

    # FUNCIÓN BOTÓN LIMPIAR
    def limpiar_formulario():
        combo_alumno.reset()
        combo_curso.reset()
        error_label.config(text="")

    b_limpiar = crear_boton(frame_botones, "Limpiar formulario", limpiar_formulario)
    b_limpiar.grid(row=0, column=2, padx=5, ipadx=5, ipady=3, sticky="ew")

    # AJUSTE DE COLUMNAS
    for i in range(3):
        frame_botones.grid_columnconfigure(i, weight=1)

#FILA 4 - TABLA DE ASIGNACIONES
    frame_tabla = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_tabla.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    tabla = treeview(frame_tabla, ["id_alumno", "id_curso"],
                    ["ID Alumno (FK)", "ID Curso (FK)"])
    TooltipTreeview(tabla)

    # FUNCION ACTUALIZAR TABLA
    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        alumnos_dict = {a[0]: a[1] for a in obtener_alumnos()}
        cursos_dict = {c[0]: c[1] for c in obtener_cursos()}
        for asignacion in obtener_alumnos_curso():
            id_alumno, id_curso = asignacion
            nombre_alumno = alumnos_dict.get(id_alumno, "Desconocido")
            nombre_curso = cursos_dict.get(id_curso, "Desconocido")
            # Guardamos los IDs como iid, y mostramos el texto con nombres
            tabla.insert(
                "", "end",
                iid=f"{id_alumno}-{id_curso}",  # iid único para la fila
                values=[f"{id_alumno} ({nombre_alumno})", f"{id_curso} ({nombre_curso})"]
            )


# MENÚ CONTEXTUAL BORRAR INSCRIPCIÓN
    menu = tk.Menu(ventana, tearoff=0)
    menu.add_command(label="Borrar inscripción...", command=borrar_seleccionado)

    # CLIC DERECHO EN TREEVIEW
    def click_derecho(event):
        item = tabla.identify_row(event.y)
        if item:
            tabla.selection_set(item)
            menu.post(event.x_root, event.y_root)

    tabla.bind("<Button-3>", click_derecho)
    tabla.bind("<Button-2>", click_derecho)

    # ACTUALIZACIÓN
    actualizar_tabla()