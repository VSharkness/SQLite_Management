import tkinter as tk
from tkinter import ttk
import re

# AUTOCOMPLETADO
class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self['values'] = self._completion_list
        self.bind('<KeyRelease>', self._on_keyrelease)

    def _on_keyrelease(self, event):
        value = self.get().lower()
        if value == '':
            data = self._completion_list
        else:
            data = [item for item in self._completion_list if value in item.lower() or item.split(" - ")[0].startswith(value)]
        self['values'] = data

    def reset(self):
        self.set("")
        self['values'] = self._completion_list

    def get_id(self):
        value = self.get().strip()
        for item in self._completion_list:
            if value.lower() == item.lower():
                m = re.match(r'^(\d+)', item)
                if m:
                    return int(m.group(1))
                return None
        if value.isdigit():
            for item in self._completion_list:
                if item.startswith(value):
                    return int(value)
        return None


# FECHA ENTRE "/"
class FechaEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.var = tk.StringVar()
        self.config(textvariable=self.var)
        self._updating = False
        self.var.trace_add("write", self.formatear_fecha)
        self.bind("<KeyPress>", self._manejar_backspace)

    def formatear_fecha(self, *args):
        if self._updating:
            return

        valor = self.var.get()
        pos_cursor = self.index(tk.INSERT)
        numeros = ''.join(filter(str.isdigit, valor))[:8]
        nuevo_valor = ""
        barras_insertadas = 0
        barra_indices = [1, 3]

        for i, digito in enumerate(numeros):
            nuevo_valor += digito
            if i in barra_indices:
                nuevo_valor += "/"
                barras_insertadas += 1
                if pos_cursor <= i + barras_insertadas:
                    pos_cursor += 1

        if self.var.get() != nuevo_valor:
            self._updating = True
            self.var.set(nuevo_valor)
            self.after(1, lambda: self.icursor(pos_cursor))
            self._updating = False

    def _manejar_backspace(self, event):
        if event.keysym == "BackSpace":
            pos = self.index(tk.INSERT)
            if pos > 0 and self.get()[pos-1] == "/":
                self.icursor(pos-1)

# TOOLTIP CURSOR
class TooltipTreeview:
    def __init__(self, treeview, delay=500):
        self.treeview = treeview
        self.delay = delay
        self.tipwindow = None
        self.id_after = None
        self.x = self.y = 0
        self.treeview.bind("<Motion>", self.on_motion)
        self.treeview.bind("<Leave>", self.on_leave)

    def on_motion(self, event):
        self.x, self.y = event.x_root + 20, event.y_root + 10
        if self.id_after:
            self.treeview.after_cancel(self.id_after)
            self.id_after = None

        region = self.treeview.identify("region", event.x, event.y)
        if region == "cell":
            rowid = self.treeview.identify_row(event.y)
            column = self.treeview.identify_column(event.x)
            if rowid and column:
                value = self.treeview.set(rowid, column)
                self.id_after = self.treeview.after(self.delay, lambda: self.showtip(value))
        else:
            self.hidetip()

    def on_leave(self, event):
        if self.id_after:
            self.treeview.after_cancel(self.id_after)
            self.id_after = None
        self.hidetip()

    def showtip(self, text):
        if self.tipwindow:
            label = self.tipwindow.winfo_children()[0]
            label.config(text=text)
            self.tipwindow.wm_geometry(f"+{self.x}+{self.y}")
            return
        self.tipwindow = tw = tk.Toplevel(self.treeview)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{self.x}+{self.y}")
        label = tk.Label(tw, text=text, justify="left",
                        background="#ffffff", relief="solid", borderwidth=1,
                        font=("Segoe UI", 9))
        label.pack(ipadx=5, ipady=2)

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None