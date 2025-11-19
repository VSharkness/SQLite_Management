#  UTILIDADES GENERALES
import tkinter as tk
from core.widgets import AutocompleteCombobox
import re


# COLORES
COLOR_FONDO ="#F7F9FC"          # Fondo general
COLOR_LABEL = "#1f2d3d"         # Texto general
COLOR_BOTON = "#C0C9E0"         # Botones
COLOR_HOVER = "#A1ABC5"         # Botones Hover
COLOR_TEXTO_BOTON = "#384052"   # Texto botones
COLOR_ERROR = "#e74c3c"         # Error
SALIR_BOTON = "#B28C8C"         # Botón Salir
SALIR_HOVER = "#A17979"         # Botón Salir Hover
SALIR_COLOR_TEXTO = "#473333"   # Texto botón Salir
COLOR_TITULO_FONDO = "#414757"  # Fondo del título
COLOR_TITULO_TEXTO = "#FFFFFF"  # Texto del título


# CENTRAR VENTANA
def centrar_ventana(ventana, ancho, alto):
    x = (ventana.winfo_screenwidth() - ancho) // 2
    y = (ventana.winfo_screenheight() - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


# VALIDACIÓN ATRIBUTOS
def validacion(entries, error_label, campos):
    def validar():
        campos_faltantes = []
        generos = []

        for entry, (nombre, articulo) in zip(entries, campos):
            # Manejo de Text
            if isinstance(entry, tk.Text):
                valor = entry.get("1.0", "end-1c").strip()
            # Manejo de AutocompleteCombobox
            elif isinstance(entry, AutocompleteCombobox):
                valor = entry.get().strip()
                if not valor or entry.get_id() is None:
                    campos_faltantes.append(nombre)
                    generos.append(articulo)
                    continue
            else:
                valor = entry.get().strip()

            if not valor:
                campos_faltantes.append(nombre)
                generos.append(articulo)

        if campos_faltantes:
            partes = [f"{g} {c}" for c, g in zip(campos_faltantes, generos)]
            mensaje_final = "Debes introducir " + "/".join(partes)
            error_label.config(text=mensaje_final, fg=COLOR_ERROR)
            return False

        error_label.config(text="")
        return True

    return validar

# VALIDACIÓN CARACTERES: LETRAS Y TILDES
def validar_nombre(P):
    return re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÜüÑñ\s\-'’]*", P) is not None


# VALIDACIÓN LÍMITE DE CARACTERES
def limitar_caracteres(entry, max_len):
    def validar(P):
        return len(P) <= max_len
    vcmd = (entry.register(validar), "%P")
    entry.config(validate="key", validatecommand=vcmd)

def limitar_caracteres_text(text_widget, max_len):
    def revisar_longitud(event=None):
        contenido = text_widget.get("1.0", "end-1c")
        if len(contenido) > max_len:
            text_widget.delete("1.0", "end")
            text_widget.insert("1.0", contenido[:max_len])
        # Resetear el flag de modificación
        text_widget.edit_modified(False)

    text_widget.bind("<<Modified>>", revisar_longitud)
    text_widget.edit_modified(False)


# VALIDACIÓN EMAIL: X@X.X
def validar_correo(correo):
    patron = r'^[^@]{1,}@[^@]{1,}\.[^@]{1,}$'
    return bool(re.match(patron, correo)) and len(correo) <= 45


# VALIDACIÓN NOTA: 2 DIGITOS (DE 0 A 10) + 1 DECIMAL
def validar_nota(nota, entrada=False):
    if entrada and nota == "":
        return True
    nota = nota.replace(",", ".")

    if not re.fullmatch(r"10|[0-9](\.\d)?", nota):
        return False

    try:
        valor = float(nota)
        return 0 <= valor <= 10
    except ValueError:
        return False


# CREAR BOTÓN
def crear_boton(frame, texto, comando=None, width=18, bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, hover_bg=COLOR_HOVER):
    b = tk.Button(frame, text=texto, command=comando, bg=bg, fg=fg,
                font=("Segoe UI", 10, "bold"), relief="flat", width=width)
    b.bind("<Enter>", lambda e: b.config(bg=hover_bg))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


# BOTONES ACCIONES (GUARDAR, BORRAR, LIMPIAR)
def botones_acciones(ventana, entries, tipo, on_save):
    def limpiar_formulario():
        for entry in entries:
            entry.delete(0, tk.END)

    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

    botones = [
        (f"Guardar {tipo}", on_save),
        ("Borrar seleccionado", None),
        ("Limpiar formulario", limpiar_formulario)
    ]

    for i in range(len(botones)):
        frame_botones.grid_columnconfigure(i, weight=1)

    for i, (texto, comando) in enumerate(botones):
        b = crear_boton(frame_botones, texto, comando)
        b.grid(row=0, column=i, padx=5, ipadx=5, ipady=3, sticky="ew")