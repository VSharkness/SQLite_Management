import tkinter as tk
from tkinter import messagebox
from core.estilos_utilidades import COLOR_FONDO, COLOR_LABEL, COLOR_ERROR, crear_boton, validacion, validar_nombre, validar_correo, centrar_ventana
from core.widgets import TooltipTreeview
from core.treeview_utilidades import treeview
from core.modales import ventana_modificar
from funciones import insertar_alumno, obtener_alumnos, actualizar_alumno, eliminar_alumno

def gestionar_alumnos(main):

    # CONFIGURACIÓN VENTANA
    ventana = tk.Toplevel(main)
    ventana.title("Gestionar alumnos")
    ventana.config(bg=COLOR_FONDO)
    centrar_ventana(ventana, 500, 430)
    ventana.resizable(False, False)
    ventana.columnconfigure(1, weight=1)

#FILA 0-1 - ENTRY Y LABEL NOMBRE/EMAIL
    nombre_entry = tk.Entry(ventana)
    correo_entry = tk.Entry(ventana)

    def longitud(P):
        return validar_nombre(P) and len(P) <= 45

    vcmd = (ventana.register(longitud), "%P")
    nombre_entry.config(validate="key", validatecommand=vcmd)

    tk.Label(ventana, text="Nombre:", bg=COLOR_FONDO, fg=COLOR_LABEL).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    nombre_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    tk.Label(ventana, text="Correo:", bg=COLOR_FONDO, fg=COLOR_LABEL).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    correo_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

#FILA 2 - LABEL DE ERROR
    error_label = tk.Label(ventana, text="", fg=COLOR_ERROR, bg=COLOR_FONDO)
    error_label.grid(row=2, column=0, columnspan=2)
    campos = [("nombre", "un"), ("correo", "un")]
    validar = validacion([nombre_entry, correo_entry], error_label, campos)

#FILA 3 - BOTONES FUNCIONALES
    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

    # FUNCIÓN BOTÓN GUARDAR
    def guardar_alumno():
        if not validar():
            return
        nombre = nombre_entry.get().strip()
        correo = correo_entry.get().strip()

        if not validar_correo(correo):
            error_label.config(text="Introduce un correo válido")
            return

        try:
            insertar_alumno(nombre, correo)
            nombre_entry.delete(0, tk.END)
            correo_entry.delete(0, tk.END)
            error_label.config(text="")
            actualizar_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el alumno:\n{e}")

    boton_guardar = crear_boton(frame_botones, "Guardar Alumno", guardar_alumno)
    boton_guardar.grid(row=0, column=0, padx=5, ipadx=5, ipady=3, sticky="ew")

    # FUNCIÓN BOTÓN BORRAR
    def borrar_seleccionado():
        selected = tabla.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un alumno", parent=ventana)
            return
        for item in selected:
            id_alumno = tabla.item(item)["values"][0]
            try:
                eliminar_alumno(id_alumno)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el alumno:\n{e}", parent=ventana)
        actualizar_tabla()

    b_borrar = crear_boton(frame_botones, "Borrar seleccionado", borrar_seleccionado)
    b_borrar.grid(row=0, column=1, padx=5, ipadx=5, ipady=3, sticky="ew")

    # FUNCIÓN BOTÓN LIMPIAR
    b_limpiar = crear_boton(frame_botones, "Limpiar formulario", lambda: [nombre_entry.delete(0, tk.END), correo_entry.delete(0, tk.END)])
    b_limpiar.grid(row=0, column=2, padx=5, ipadx=5, ipady=3, sticky="ew")

    # AJUSTE DE COLUMNAS
    for i in range(3):
        frame_botones.grid_columnconfigure(i, weight=1)

#FILA 4 - TABLA DE ALUMNOS
    frame_tabla = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_tabla.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    tabla = treeview(frame_tabla, ["id", "nombre", "correo"], ["ID", "Nombre", "Correo"])
    TooltipTreeview(tabla)

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for alumno in obtener_alumnos():
            tabla.insert("", "end", values=alumno)

    menu = tk.Menu(ventana, tearoff=0)
    
    # MODIFICAR REGISTRO
    def modificar_alumno():
        selected = tabla.selection()
        if not selected:
            return
        item = selected[0]
        alumno = tabla.item(item)["values"]

        # Función para validar nombre en la modal
        def longitud(P):
            return validar_nombre(P) and len(P) <= 45

        def guardar(id_alumno, nombre, correo):
            actualizar_alumno(id_alumno, nombre=nombre, correo=correo)
            actualizar_tabla()

        # Pasamos la función de validación para nombre
        ventana_modificar(
            ventana,
            alumno,
            [("nombre", "Nombre", longitud), ("correo", "Correo")],
            guardar
        )
    
    menu.add_command(label="Modificar registro...", command=modificar_alumno)

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