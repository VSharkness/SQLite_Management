from tkinter import ttk


# TREEVIEW: TABLA
def treeview(frame, columnas, encabezados):
    style = ttk.Style()
    style.configure("Custom.Treeview",
                    background="white",
                    foreground="black",
                    rowheight=24,
                    fieldbackground="white",
                    bordercolor="#ccc",
                    borderwidth=1)
    style.configure("Custom.Treeview.Heading",
                    background="#dfe3e8",
                    foreground="#333",
                    font=("Segoe UI", 10, "bold"))

    tree = ttk.Treeview(frame, columns=columnas, show="headings", height=10, style="Custom.Treeview")

    for col, head in zip(columnas, encabezados):
        tree.heading(col, text=head, command=lambda _col=col: treeview_sort_column(tree, _col, False))
        if col.lower() == "id":
            width = 40
        elif col.lower() in ["descripcion", "descripción"]:
            width = 220
        else:
            width = 160
        tree.column(col, width=width, anchor="center")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    return tree


# ORDENAR TABLA
def treeview_sort_column(tv, col, reverse):
    try:
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            l.sort(key=lambda t: t[0].lower(), reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))
    except Exception as e:
        print(f"Error ordenando columna {col}: {e}")

