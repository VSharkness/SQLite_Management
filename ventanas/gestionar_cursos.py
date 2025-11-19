import tkinter as tk
from tkinter import messagebox
from core.estilos_utilidades import COLOR_FONDO, COLOR_LABEL, COLOR_ERROR, crear_boton, validacion, centrar_ventana, limitar_caracteres, limitar_caracteres_text
from core.widgets import TooltipTreeview
from core.treeview_utilidades import treeview
from core.modales import ventana_modificar
from funciones import insertar_curso, obtener_cursos, actualizar_curso, eliminar_curso

def gestionar_cursos(main):

    # CONFIGURACIÓN VENTANA
    ventana = tk.Toplevel(main)
    ventana.title("Gestionar Cursos")
    ventana.config(bg=COLOR_FONDO)
    centrar_ventana(ventana, 500, 500)
    ventana.resizable(False, False)
    ventana.columnconfigure(1, weight=1)

#FILA 0-1 - ENTRY Y LABEL NOMBRE/DESCRIPCIÓN
    nombre_entry = tk.Entry(ventana)
    descripcion_entry = tk.Text(ventana, height=5, width=40)
    descripcion_entry.grid(row=1, column=1, padx=10, pady=(5,0), sticky="ew")
    MAX_CHARS = 200

    limitar_caracteres_text(descripcion_entry, 200)
    limitar_caracteres(nombre_entry, 45)

    tk.Label(ventana, text="Nombre:", bg=COLOR_FONDO, fg=COLOR_LABEL).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    nombre_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    tk.Label(ventana, text="Descripción:", bg=COLOR_FONDO, fg=COLOR_LABEL).grid(row=1, column=0, padx=10, pady=5, sticky="e")

#FILA 2 - CONTADOR DE CARACTERES
    contador_label = tk.Label(ventana, text=f"0/{MAX_CHARS}", bg=COLOR_FONDO, fg=COLOR_LABEL)
    contador_label.grid(row=2, column=1, sticky="e", padx=10, pady=(2,5))

    # FUNCIÓN PARA ACTUALIZAR EL CONTADOR
    def actualizar_contador(event=None):
        contenido = descripcion_entry.get("1.0", "end-1c")
        if len(contenido) > MAX_CHARS:
            # RECORTA A MAX_CHARS
            descripcion_entry.delete("1.0", "end")
            descripcion_entry.insert("1.0", contenido[:MAX_CHARS])
            contenido = contenido[:MAX_CHARS]
        contador_label.config(text=f"{len(contenido)}/{MAX_CHARS}")
        descripcion_entry.edit_modified(False)

    descripcion_entry.bind("<<Modified>>", actualizar_contador)
    descripcion_entry.edit_modified(False)

#FILA 3 - LABEL DE ERROR
    error_label = tk.Label(ventana, text="", fg=COLOR_ERROR, bg=COLOR_FONDO)
    error_label.grid(row=2, column=0, columnspan=2)
    campos = [("nombre", "un"), ("descripción", "una")]
    validar = validacion([nombre_entry, descripcion_entry], error_label, campos)

#FILA 4 - BOTONES FUNCIONALES
    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

    # FUNCIÓN BOTÓN GUARDAR
    def guardar_curso():
        if not validar():
            return
        nombre = nombre_entry.get().strip()
        descripcion = descripcion_entry.get("1.0", "end-1c").strip()
        try:
            insertar_curso(nombre, descripcion)
            nombre_entry.delete(0, tk.END)
            descripcion_entry.delete("1.0", "end")
            error_label.config(text="")
            actualizar_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el curso:\n{e}")

    boton_guardar = crear_boton(frame_botones, f"Guardar Curso", guardar_curso)
    boton_guardar.grid(row=0, column=0, padx=5, ipadx=5, ipady=3, sticky="ew")

    # FUNCIÓN BOTÓN BORRAR
    def borrar_seleccionado():
        selected = tabla.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un curso", parent=ventana)
            return
        for item in selected:
            id_curso = tabla.item(item)["values"][0]
            try:
                eliminar_curso(id_curso)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el curso:{e}", parent=ventana)
        actualizar_tabla()

    b_borrar = crear_boton(frame_botones, "Borrar seleccionado", borrar_seleccionado)
    b_borrar.grid(row=0, column=1, padx=5, sticky="ew")

    # FUNCIÓN BOTÓN LIMPIAR
    b_limpiar = crear_boton(frame_botones, "Limpiar formulario", lambda: [nombre_entry.delete(0, tk.END), descripcion_entry.delete(0, tk.END)])
    b_limpiar.grid(row=0, column=2, padx=5, sticky="ew")

    # AJUSTE DE COLUMNAS
    for i in range(3):
        frame_botones.grid_columnconfigure(i, weight=1)

#FILA 5 - TABLA DE CURSOS
    frame_tabla = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_tabla.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    tabla = treeview(frame_tabla, ["id", "nombre", "descripcion"], ["ID", "Nombre", "Descripción"])
    TooltipTreeview(tabla)

    # FUNCION ACTUALIZAR TABLA
    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for curso in obtener_cursos():
            tabla.insert("", "end", values=curso)

# MENÚ CONTEXTUAL MODIFICAR
    menu = tk.Menu(ventana, tearoff=0)

    # FUNCIÓN MODIFICAR CURSO
    def modificar_curso():
        selected = tabla.selection()
        if not selected:
            return
        item = selected[0]
        curso = tabla.item(item)["values"]

        def guardar(id_curso, nombre, descripcion):
            actualizar_curso(id_curso, nombre=nombre, descripcion=descripcion)
            actualizar_tabla()

        ventana_modificar(ventana, curso, [("nombre", "Nombre"), ("descripcion", "Descripción")], guardar)

    menu.add_command(label="Modificar registro...", command=modificar_curso)

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