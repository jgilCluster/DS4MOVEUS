# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 16:38:10 2026

@author: JonGilAlvaro
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# ================= VENTANA PRINCIPAL =================
root = tk.Tk()
root.title("Monitorización - Data Categories")
root.geometry("600x500")

tree = ttk.Treeview(root, columns=("datasets"), show="tree headings")
tree.heading("#0", text="Categoría / Subcategoría / Conector", anchor="w")
tree.heading("datasets", text="Total Datasets", anchor="center")
tree.column("#0", width=450)
tree.column("datasets", width=150, anchor="center")
tree.pack(fill="both", expand=True, padx=10, pady=10)

# ================= DATOS =================
conectores = {
    "Conector 1": 15,
    "Conector 2": 25,
    "Conector 3": 10,
    "Conector 4": 20,
}

datos = {
    "Parking": {
        "Aparcamiento": ["Conector 1", "Conector 2", "Conector 4"],
        "OTA": ["Conector 2", "Conector 3"],
        "P Camiones": ["Conector 1", "Conector 3", "Conector 4"],
    },
    "Tráfico": {
        "Peaje": ["Conector 1", "Conector 2"],
        "Cámaras Carretera": ["Conector 2", "Conector 3", "Conector 4"],
        "Matrices O-D": ["Conector 1", "Conector 3"],
    }
}

# ================= VARIABLES GLOBALES =================
totales_globales = {c: 0 for c in conectores}

# ================= FUNCIONES =================
def construir_categoria(nombre, subcats):
    """
    Inserta una categoría completa en el TreeView
    y suma los valores a totales_globales
    """
    cat_id = tree.insert("", "end", text=nombre, values=(0,), open=False)
    total_categoria = 0

    for sub, cons in subcats.items():
        total_subcategoria = 0
        sub_id = tree.insert(cat_id, "end", text=sub, values=(0,))
        for c in cons:
            valor = conectores[c]
            tree.insert(sub_id, "end", text=c, values=(valor,))
            total_subcategoria += valor
            # Sumar al global
            totales_globales[c] += valor
        tree.item(sub_id, values=(total_subcategoria,))
        total_categoria += total_subcategoria

    tree.item(cat_id, values=(total_categoria,))
    return total_categoria

def refrescar_tree_principal():
    """Reconstruye todo el Treeview principal con totales actualizados"""
    tree.delete(*tree.get_children())
    # Reiniciar totales globales
    for c in totales_globales:
        totales_globales[c] = 0
    # Reconstruir categorías
    for cat_name, subcats in datos.items():
        construir_categoria(cat_name, subcats)
    # Nodo TOTAL
    suma_total = sum(totales_globales.values())
    total_id = tree.insert("", "end", text="TOTAL", values=(suma_total,), open=False)
    for c, v in totales_globales.items():
        tree.insert(total_id, "end", text=c, values=(v,))

# ================= TREE PRINCIPAL =================
refrescar_tree_principal()

# ================= GRAFICAS =================
def abrir_graficas():
    win = tk.Toplevel(root)
    win.title("Gráficas de Monitorización")
    win.geometry("450x420")

    # ---- Categoría ----
    tk.Label(win, text="Categoría").pack()
    categoria_cb = ttk.Combobox(win, values=["TODAS"] + list(datos.keys()), state="readonly")
    categoria_cb.current(0)
    categoria_cb.pack(pady=4)

    # ---- Subcategoría ----
    tk.Label(win, text="Subcategoría").pack()
    subcat_cb = ttk.Combobox(win, values=["TODAS"], state="readonly")
    subcat_cb.current(0)
    subcat_cb.pack(pady=4)

    def actualizar_subcats(event=None):
        cat = categoria_cb.get()
        if cat == "TODAS":
            subcat_cb["values"] = ["TODAS"]
        else:
            subcat_cb["values"] = ["TODAS"] + list(datos[cat].keys())
        subcat_cb.current(0)

    categoria_cb.bind("<<ComboboxSelected>>", actualizar_subcats)

    # ---- Conectores ----
    tk.Label(win, text="Conectores").pack(pady=5)
    frame_checks = tk.Frame(win)
    frame_checks.pack()
    vars_conectores = {}
    for c in conectores:
        v = tk.BooleanVar(value=True)
        vars_conectores[c] = v
        tk.Checkbutton(frame_checks, text=c, variable=v).pack(anchor="w")

    # ---- Tipo grafico ----
    tk.Label(win, text="Tipo de gráfico").pack(pady=5)
    tipo_grafico = ttk.Combobox(win, values=["Barras", "Circular"], state="readonly")
    tipo_grafico.current(0)
    tipo_grafico.pack()

    # ---- Generar ----
    def generar():
        seleccionados = [c for c, v in vars_conectores.items() if v.get()]
        if not seleccionados:
            seleccionados = list(conectores.keys())

        acumulado = {c: 0 for c in seleccionados}
        for cat, subcats in datos.items():
            if categoria_cb.get() != "TODAS" and cat != categoria_cb.get():
                continue
            for sub, cons in subcats.items():
                if subcat_cb.get() != "TODAS" and sub != subcat_cb.get():
                    continue
                for c in cons:
                    if c in seleccionados:
                        acumulado[c] += conectores[c]

        labels = [c for c, v in acumulado.items() if v > 0]
        values = [v for v in acumulado.values() if v > 0]

        plt.figure(figsize=(4, 4))
        cat_sel = categoria_cb.get()
        sub_sel = subcat_cb.get()
        if cat_sel == "TODAS":
            subtitulo = "Categoría: TODAS"
        elif sub_sel == "TODAS":
            subtitulo = f"Categoría: {cat_sel} - Subcategoría: TODAS"
        else:
            subtitulo = f"Categoría: {cat_sel} - Subcategoría: {sub_sel}"

        if tipo_grafico.get() == "Barras":
            plt.bar(labels, values)
            plt.ylabel("Datasets Consumidos")
            plt.title("Total de Datasets por Conector\n" + subtitulo)
        else:
            plt.pie(values, labels=labels,
                    autopct=lambda p: f"{int(round(p * sum(values) / 100))}",
                    startangle=90)
            plt.title("Total de Datasets por Conector\n" + subtitulo)

        plt.tight_layout()
        plt.show()

    tk.Button(win, text="Generar Gráfica", command=generar).pack(pady=15)

# ================= EDITAR CATEGORIAS =================
def editar_categorias():
    win_edit = tk.Toplevel(root)
    win_edit.title("Editar Categorías")
    win_edit.geometry("500x450")  # un poco más grande para los botones adicionales

    tree_edit = ttk.Treeview(win_edit, columns=("accion"), show="tree headings")
    tree_edit.heading("#0", text="Categoría / Subcategoría", anchor="w")
    tree_edit.heading("accion", text="Acción", anchor="center")
    tree_edit.column("#0", width=300)
    tree_edit.column("accion", width=100, anchor="center")
    tree_edit.pack(fill="both", expand=True, padx=10, pady=10)

    botones_modificar = {}

    def refrescar_tree_edit():
        tree_edit.delete(*tree_edit.get_children())
        botones_modificar.clear()
        for cat, subcats in datos.items():
            cat_id = tree_edit.insert("", "end", text=cat, values=("Modificar",))
            botones_modificar[cat_id] = ("cat", cat)
            for sub in subcats:
                sub_id = tree_edit.insert(cat_id, "end", text=sub, values=("Modificar",))
                botones_modificar[sub_id] = ("sub", cat, sub)

    def abrir_modificar(event):
        item = tree_edit.selection()
        if not item:
            return
        item_id = item[0]
        tipo = botones_modificar[item_id][0]

        win_mod = tk.Toplevel(win_edit)
        win_mod.title("Modificar")
        win_mod.geometry("350x150")

        tk.Label(win_mod, text="Nombre actual:").pack(pady=5)
        actual = botones_modificar[item_id][1] if tipo=="cat" else botones_modificar[item_id][2]
        tk.Label(win_mod, text=actual, fg="blue").pack()
        tk.Label(win_mod, text="Nuevo nombre:").pack(pady=5)

        nuevo_entry = tk.Entry(win_mod)
        nuevo_entry.pack()
        nuevo_entry.insert(0, actual)

        def guardar_cambio():
            global totales_globales
            nuevo = nuevo_entry.get().strip()
            if not nuevo:
                messagebox.showwarning("Aviso", "El nombre no puede estar vacío")
                return

            if tipo == "cat":
                old = botones_modificar[item_id][1]
                datos[nuevo] = datos.pop(old)
            else:
                cat_name = botones_modificar[item_id][1]
                sub_name = botones_modificar[item_id][2]
                datos[cat_name][nuevo] = datos[cat_name].pop(sub_name)

            refrescar_tree_edit()
            refrescar_tree_principal()
            win_mod.destroy()

        tk.Button(win_mod, text="Guardar", command=guardar_cambio).pack(pady=10)

    tree_edit.bind("<Double-1>", abrir_modificar)

    # ---- Botones de Añadir ----
    frame_botones_add = tk.Frame(win_edit)
    frame_botones_add.pack(pady=10)

    # --- Añadir Categoría ---
    def agregar_categoria():
        win_add_cat = tk.Toplevel(win_edit)
        win_add_cat.title("Añadir Categoría")
        win_add_cat.geometry("300x120")

        tk.Label(win_add_cat, text="Nombre de la nueva categoría:").pack(pady=5)
        entry_cat = tk.Entry(win_add_cat)
        entry_cat.pack()
        
        def guardar_categoria():
            nuevo_cat = entry_cat.get().strip()
            if not nuevo_cat:
                messagebox.showwarning("Aviso", "El nombre no puede estar vacío")
                return
            if nuevo_cat in datos:
                messagebox.showwarning("Aviso", "La categoría ya existe")
                return
            datos[nuevo_cat] = {}  # nueva categoría vacía
            refrescar_tree_edit()
            refrescar_tree_principal()
            win_add_cat.destroy()

        tk.Button(win_add_cat, text="Añadir Categoría", command=guardar_categoria).pack(pady=10)

    tk.Button(frame_botones_add, text="Añadir Categoría", command=agregar_categoria).pack(side="left", padx=5)

    # --- Añadir Subcategoría ---
    def agregar_subcategoria():
        win_add_sub = tk.Toplevel(win_edit)
        win_add_sub.title("Añadir Subcategoría")
        win_add_sub.geometry("350x150")

        tk.Label(win_add_sub, text="Selecciona la categoría:").pack(pady=5)
        cat_cb = ttk.Combobox(win_add_sub, values=list(datos.keys()), state="readonly")
        if datos:
            cat_cb.current(0)
        cat_cb.pack()

        tk.Label(win_add_sub, text="Nombre de la nueva subcategoría:").pack(pady=5)
        entry_sub = tk.Entry(win_add_sub)
        entry_sub.pack()

        def guardar_subcategoria():
            cat_sel = cat_cb.get()
            sub_nombre = entry_sub.get().strip()
            if not sub_nombre:
                messagebox.showwarning("Aviso", "El nombre no puede estar vacío")
                return
            if sub_nombre in datos[cat_sel]:
                messagebox.showwarning("Aviso", "La subcategoría ya existe en esta categoría")
                return
            datos[cat_sel][sub_nombre] = []  # subcategoría nueva sin conectores
            refrescar_tree_edit()
            refrescar_tree_principal()
            win_add_sub.destroy()

        tk.Button(win_add_sub, text="Añadir Subcategoría", command=guardar_subcategoria).pack(pady=10)

    tk.Button(frame_botones_add, text="Añadir Subcategoría", command=agregar_subcategoria).pack(side="left", padx=5)

    # Finalmente refrescamos el tree al abrir
    refrescar_tree_edit()

# ================= BOTONES =================
frame_botones = tk.Frame(root)
frame_botones.pack(pady=5)

tk.Button(frame_botones, text="Graficar", command=abrir_graficas).pack(side="left", padx=5)
tk.Button(frame_botones, text="EDITAR CATEGORIAS", command=editar_categorias).pack(side="left", padx=5)

root.mainloop()
