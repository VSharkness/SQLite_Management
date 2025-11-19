import tkinter as tk
from tkinter import messagebox
from core.estilos_utilidades import COLOR_FONDO, COLOR_LABEL, COLOR_ERROR, crear_boton, validacion, centrar_ventana, limitar_caracteres
from core.widgets import TooltipTreeview, AutocompleteCombobox, FechaEntry
from core.treeview_utilidades import treeview
from core.modales import ventana_modificar
from funciones import insertar_tarea, obtener_tareas, actualizar_tarea, eliminar_tarea, obtener_cursos

def gestionar_tareas(main):

    # CONFIGURACIÓN VENTANA
    ventana = tk.Toplevel(main)
    ventana.title("Gestionar tareas")
    ventana.config(bg=COLOR_FONDO)
    centrar_ventana(ventana, 800, 460)
    ventana.resizable(False, False)
    ventana.columnconfigure(1, weight=1)

#FILA 0-2 - ENTRY Y LABEL CURSO/TÍTULO/FECHA
    tk.Label(ventana, text="Curso:", bg=COLOR_FONDO, fg=COLOR_LABEL).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    combo_curso = AutocompleteCombobox(ventana, state="normal")
    combo_curso.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    combo_curso.set_completion_list([f"{c[0]} ({c[1]})" for c in obtener_cursos()])

    tk.Label(ventana, text="Título:", bg=COLOR_FONDO, fg=COLOR_LABEL).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    titulo_entry = tk.Entry(ventana)
    limitar_caracteres(titulo_entry, 45)
    titulo_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(ventana, text="Entrega:", bg=COLOR_FONDO, fg=COLOR_LABEL).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    fecha_entry = FechaEntry(ventana)
    fecha_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

#FILA 3 - LABEL DE ERROR
    error_label = tk.Label(ventana, text="", fg=COLOR_ERROR, bg=COLOR_FONDO)
    error_label.grid(row=3, column=0, columnspan=2)
    campos = [("curso", "un"), ("título", "un"), ("entrega", "una")]
    validar = validacion([combo_curso, titulo_entry, fecha_entry], error_label, campos)

#FILA 4 - BOTONES FUNCIONALES
    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

    # FUNCIÓN BOTÓN GUARDAR
    def guardar_tarea():
        if not validar():
            return
        id_curso = combo_curso.get_id()
        titulo = titulo_entry.get().strip()
        fecha = fecha_entry.get().strip()
        try:
            insertar_tarea(titulo, fecha, id_curso)
            titulo_entry.delete(0, tk.END)
            fecha_entry.delete(0, tk.END)
            error_label.config(text="")
            actualizar_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la tarea:\n{e}")

    # FUNCIÓN BOTÓN BORRAR
    def borrar_seleccionado():
        selected = tabla.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona una tarea", parent=ventana)
            return
        for item in selected:
            id_tarea = tabla.item(item)["values"][0]
            try:
                eliminar_tarea(id_tarea)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la tarea:\n{e}", parent=ventana)
        actualizar_tabla()

    # BOTONES
    boton_guardar = crear_boton(frame_botones, "Guardar Tarea", guardar_tarea)
    boton_guardar.grid(row=0, column=0, padx=5, ipadx=5, ipady=3, sticky="ew")

    b_borrar = crear_boton(frame_botones, "Borrar seleccionado", borrar_seleccionado)
    b_borrar.grid(row=0, column=1, padx=5, ipadx=5, ipady=3, sticky="ew")

    b_limpiar = crear_boton(frame_botones, "Limpiar formulario", lambda: [titulo_entry.delete(0, tk.END), fecha_entry.delete(0, tk.END)])
    b_limpiar.grid(row=0, column=2, padx=5, ipadx=5, ipady=3, sticky="ew")

    for i in range(3):
        frame_botones.grid_columnconfigure(i, weight=1)

#FILA 5 - TABLA DE TAREAS
    frame_tabla = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_tabla.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    tabla = treeview(frame_tabla, ["id", "titulo", "fecha", "curso"], ["ID", "Título", "Entrega", "ID Curso (FK)"])
    TooltipTreeview(tabla)

    # FUNCION ACTUALIZAR TABLA
    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        cursos_dict = {c[0]: c[1] for c in obtener_cursos()}
        for tarea in obtener_tareas():
            id_tarea, titulo, fecha, id_curso = tarea
            valor_curso = f"{id_curso} ({cursos_dict.get(id_curso, 'Desconocido')})"
            tabla.insert("", "end", values=[id_tarea, titulo, fecha, valor_curso])

# MENÚ CONTEXTUAL MODIFICAR
    menu = tk.Menu(ventana, tearoff=0)

    # FUNCIÓN MODIFICAR TAREA
    def modificar_tarea():
        selected = tabla.selection()
        if not selected:
            return
        item = selected[0]
        tarea = tabla.item(item)["values"]

        # CALLBACK GUARDAR CAMBIOS
        def guardar(id_tarea, titulo, fecha):
            actualizar_tarea(id_tarea, titulo=titulo, fecha_entrega=fecha)
            actualizar_tabla()

        ventana_modificar(ventana, tarea, [("titulo", "Título"), ("fecha", "Entrega")], guardar)

    menu.add_command(label="Modificar registro...", command=modificar_tarea)

# CLIC DERECHO EN TREEVIEW
    def click_derecho(event):
        item = tabla.identify_row(event.y)
        if item:
            tabla.selection_set(item)
            menu.post(event.x_root, event.y_root)

    tabla.bind("<Button-3>", click_derecho)  # Windows/Linux
    tabla.bind("<Button-2>", click_derecho)  # Mac

    # ACTUALIZACIÓN
    actualizar_tabla()