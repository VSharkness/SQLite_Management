import tkinter as tk
from tkinter import messagebox
from core.estilos_utilidades import COLOR_FONDO, COLOR_LABEL, COLOR_ERROR, crear_boton, validacion, centrar_ventana, validar_nota
from core.widgets import TooltipTreeview, AutocompleteCombobox, FechaEntry
from core.treeview_utilidades import treeview
from core.modales import ventana_modificar
from funciones import insertar_entrega, obtener_entregas, actualizar_entrega, eliminar_entrega, obtener_alumnos, obtener_tareas

def gestionar_entregas(main):

    # CONFIGURACIÓN VENTANA
    ventana = tk.Toplevel(main)
    ventana.title("Gestionar entregas")
    ventana.config(bg=COLOR_FONDO)
    centrar_ventana(ventana, 800, 490)
    ventana.resizable(False, False)
    ventana.columnconfigure(1, weight=1)

#FILA 0-3 - ENTRY Y LABEL ALUMNO/TAREA/FECHA/NOTA
    tk.Label(ventana, text="Alumno:", bg=COLOR_FONDO, fg=COLOR_LABEL).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    combo_alumno = AutocompleteCombobox(ventana, state="normal")
    combo_alumno.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    combo_alumno.set_completion_list([f"{a[0]} ({a[1]})" for a in obtener_alumnos()])

    tk.Label(ventana, text="Tarea:", bg=COLOR_FONDO, fg=COLOR_LABEL).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    combo_tarea = AutocompleteCombobox(ventana, state="normal")
    combo_tarea.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    combo_tarea.set_completion_list([f"{t[0]} ({t[1]})" for t in obtener_tareas()])

    fecha_entry = FechaEntry(ventana)
    nota_entry = tk.Entry(ventana)
    vcmd_nota = (ventana.register(lambda P: validar_nota(P, entrada=True)), "%P")
    nota_entry.config(validate="key", validatecommand=vcmd_nota)

    tk.Label(ventana, text="Fecha de envío:", bg=COLOR_FONDO, fg=COLOR_LABEL).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    fecha_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(ventana, text="Nota:", bg=COLOR_FONDO, fg=COLOR_LABEL).grid(row=3, column=0, padx=10, pady=5, sticky="e")
    nota_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

#FILA 4 - LABEL DE ERROR
    error_label = tk.Label(ventana, text="", fg=COLOR_ERROR, bg=COLOR_FONDO)
    error_label.grid(row=4, column=0, columnspan=2)
    campos = [("fecha", "una"), ("nota", "una")]
    validar = validacion([fecha_entry, nota_entry], error_label, campos)

#FILA 5 - BOTONES FUNCIONALES
    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")

    campos = [("alumno", "un"), ("tarea", "una"), ("fecha", "una"), ("nota", "una")]
    validar = validacion([combo_alumno, combo_tarea, fecha_entry, nota_entry], error_label, campos)

    # FUNCIÓN BOTÓN GUARDAR
    def guardar_entrega():
        if not validar():
            return

        id_alumno = combo_alumno.get_id()
        id_tarea = combo_tarea.get_id()
        fecha = fecha_entry.get().strip()
        nota = nota_entry.get().strip()

        if not id_alumno or not id_tarea:
            error_label.config(text="Selecciona un alumno y una tarea válidos")
            return
        if not fecha:
            error_label.config(text="Introduce una fecha")
            return
        if not validar_nota(nota):
            error_label.config(text="Introduce una nota válida (0-10, 1 decimal máximo)")
            return

        try:
            insertar_entrega(id_alumno, id_tarea, fecha, nota)
            combo_alumno.set("")
            combo_tarea.set("")
            fecha_entry.delete(0, tk.END)
            nota_entry.delete(0, tk.END)
            error_label.config(text="")
            actualizar_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la entrega:\n{e}")

    boton_guardar = crear_boton(frame_botones, f"Guardar Entrega", guardar_entrega)
    boton_guardar.grid(row=0, column=0, padx=5, ipadx=5, ipady=3, sticky="ew")

    # FUNCIÓN BOTÓN BORRAR
    def borrar_seleccionado():
        selected = tabla.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona una entrega", parent=ventana)
            return
        for item in selected:
            id_entrega = tabla.item(item)["values"][0]
            try:
                eliminar_entrega(id_entrega)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la entrega:\n{e}", parent=ventana)
        actualizar_tabla()

    b_borrar = crear_boton(frame_botones, "Borrar seleccionado", borrar_seleccionado)
    b_borrar.grid(row=0, column=1, padx=5, ipadx=5, ipady=3, sticky="ew")

    # FUNCIÓN BOTÓN LIMPIAR
    b_limpiar = crear_boton(frame_botones, "Limpiar formulario", lambda: [fecha_entry.delete(0, tk.END), nota_entry.delete(0, tk.END), combo_alumno.set(""), combo_tarea.set("")])
    b_limpiar.grid(row=0, column=2, padx=5, ipadx=5, ipady=3, sticky="ew")

    # AJUSTE DE COLUMNAS
    for i in range(3):
        frame_botones.grid_columnconfigure(i, weight=1)

#FILA 6 - TABLA DE ENTREGAS
    frame_tabla = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_tabla.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    tabla = treeview(frame_tabla, ["id", "fecha", "nota", "alumno", "tarea"], ["ID", "Fecha de envío", "Nota", "ID Alumno (FK)", "ID Tarea (FK)"])
    TooltipTreeview(tabla)

    # FUNCION ACTUALIZAR TABLA
    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        alumnos_dict = {a[0]: a[1] for a in obtener_alumnos()}
        tareas_dict = {t[0]: t[1] for t in obtener_tareas()}
        for entrega in obtener_entregas():
            id_entrega, fecha, nota, id_alumno, id_tarea = entrega
            valor_alumno = f"{id_alumno} ({alumnos_dict.get(id_alumno, 'Desconocido')})"
            valor_tarea = f"{id_tarea} ({tareas_dict.get(id_tarea, 'Desconocido')})"
            tabla.insert("", "end", values=[id_entrega, fecha, nota, valor_alumno, valor_tarea])

# MENÚ CONTEXTUAL MODIFICAR
    menu = tk.Menu(ventana, tearoff=0)

    # FUNCIÓN MODIFICAR ENTREGA
    def modificar_entrega():
        selected = tabla.selection()
        if not selected:
            return
        item = selected[0]
        entrega = tabla.item(item)["values"]

        def guardar(id_entrega, fecha, nota):
            actualizar_entrega(id_entrega, fecha_envio=fecha, nota=nota)
            actualizar_tabla()

        ventana_modificar(ventana, entrega, [("fecha", "Fecha"), ("nota", "Nota")], guardar)

    menu.add_command(label="Modificar registro...", command=modificar_entrega)

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