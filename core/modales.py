import tkinter as tk
import re
from core.estilos_utilidades import COLOR_FONDO, COLOR_LABEL, COLOR_ERROR, centrar_ventana, crear_boton, validar_correo, limitar_caracteres, limitar_caracteres_text


# MODAL PARA MODIFICAR ATRIBUTO
def ventana_modificar(parent, valores, campos, on_guardar):
    modal = tk.Toplevel(parent)
    modal.title("Modificar registro")
    modal.config(bg=COLOR_FONDO)
    modal.resizable(True, False)
    
    alto = 80 + len(campos)*25 + 20
    if any(c[0].lower() in ["descripcion", "descripción"] for c in campos):
        alto += 50
    ancho = 400
    centrar_ventana(modal, ancho, alto)

    entries = []
    contador_label = None
    tiene_text = any(c[0].lower() in ["descripcion", "descripción"] for c in campos)

    for i, campo in enumerate(campos):
        nombre, label_text = campo[:2]

        fila = tk.Frame(modal, bg=COLOR_FONDO)
        fila.pack(fill="x", padx=0, pady=5)
        tk.Label(fila, text=label_text + ":", bg=COLOR_FONDO, fg=COLOR_LABEL, width=10, anchor="e").pack(side="left")

        # DECIDIR QUÉ WIDGET USAR
        if nombre.lower() in ["descripcion", "descripción"]:
            frame_text = tk.Frame(fila, bg=COLOR_FONDO)
            frame_text.pack(side="left", fill="both", expand=True)

            widget = tk.Text(frame_text, height=5, width=40)
            widget.pack(fill="both", expand=True)
            widget.insert("1.0", valores[i+1])
            limitar_caracteres_text(widget, 200)

            contador_label = tk.Label(frame_text, text=f"{len(valores[i+1])}/200", bg=COLOR_FONDO, fg=COLOR_LABEL, anchor="e")
            contador_label.pack(fill="x", pady=(2,0))

            def actualizar_contador(event=None, w=widget, l=contador_label):
                contenido = w.get("1.0", "end-1c")
                if len(contenido) > 200:
                    w.delete("1.0", "end")
                    w.insert("1.0", contenido[:200])
                    contenido = contenido[:200]
                l.config(text=f"{len(contenido)}/200")
                w.edit_modified(False)

            widget.bind("<<Modified>>", actualizar_contador)
            widget.edit_modified(False)

        else:
            widget = tk.Entry(fila, justify="left")
            widget.insert(0, valores[i+1])
            widget.pack(side="left", fill="x", expand=True)

            if nombre.lower() == "nota":
                def validar_entrada(P):
                    if P == "":
                        return True
                    valor = P.replace(",", ".")
                    if re.fullmatch(r"(10(\.0?)?|[0-9](\.\d?)?)", valor):
                        try:
                            return float(valor) <= 10
                        except:
                            return False
                    return False
                vcmd = (modal.register(validar_entrada), "%P")
                widget.config(validate="key", validatecommand=vcmd)

            if nombre.lower() == "nombre":
                limitar_caracteres(widget, 45)

        entries.append((nombre.lower(), widget))

    error_label = None
    if not tiene_text:
        error_label = tk.Label(modal, text="", fg=COLOR_ERROR, bg=COLOR_FONDO)
        error_label.pack(fill="x", padx=10, pady=(0, 5))

    frame_botones = tk.Frame(modal, bg=COLOR_FONDO)
    frame_botones.pack(fill="x", pady=10, padx=0)

    b_aceptar = crear_boton(frame_botones, "Modificar",
                            lambda: aceptar(entries, valores[0], on_guardar, modal, error_label))
    b_aceptar.pack(side="left", expand=True, fill="x", padx=5)
    b_cancelar = crear_boton(frame_botones, "Cancelar", modal.destroy)
    b_cancelar.pack(side="left", expand=True, fill="x", padx=5)


# APLICAR MODIFICACIONES
def aceptar(entries, id_valor, on_guardar, modal, error_label):
    nuevos_valores = []
    for nombre, e in entries:
        texto = e.get().strip() if not isinstance(e, tk.Text) else e.get("1.0", "end-1c").strip()
        if nombre == "fecha":
            match = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", texto)
            if not match:
                if error_label:
                    error_label.config(text="Fecha inválida. Debe ser DD/MM/YYYY")
                return
            dia, mes, año = match.groups()
            texto = f"{int(dia):02d}/{int(mes):02d}/{año}"
        nuevos_valores.append(texto)

    # Validación campos obligatorios y correo
    if error_label:
        if any(not v for v in nuevos_valores):
            error_label.config(text="Todos los campos son obligatorios")
            return
        if len(nuevos_valores) > 1 and "@" in nuevos_valores[1]:
            if not validar_correo(nuevos_valores[1]):
                error_label.config(text="Correo inválido")
                return

    try:
        on_guardar(id_valor, *nuevos_valores)
        modal.destroy()
    except Exception as e:
        if error_label:
            error_label.config(text=f"No se pudo guardar:\n{e}")
