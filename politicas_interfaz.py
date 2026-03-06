# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 21:26:16 2026

@author: jongi
"""

import tkinter as tk
from tkinter import ttk, messagebox


# ---------------- UTILIDADES ----------------
def copiar_al_portapapeles(root, texto):
    root.clipboard_clear()
    root.clipboard_append(texto)
    root.update()


# ---------------- VENTANA AUTENTICACIÓN ----------------
def pedir_credenciales(root, on_success):
    ventana = tk.Toplevel(root)
    ventana.title("Autenticación requerida")
    ventana.geometry("400x320")
    ventana.grab_set()  # ventana modal

    frame = ttk.Frame(ventana, padding=15)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="Al tratarse de información sensible\n"
             "debe introducir usuario y contraseña\n"
             "de administrador",
        justify="center",
        font=("Arial", 10, "bold")
    ).pack(pady=10)

    ttk.Label(frame, text="Usuario").pack(anchor="w")
    entry_user = ttk.Entry(frame)
    entry_user.pack(fill="x", pady=5)

    ttk.Label(frame, text="Contraseña").pack(anchor="w")
    entry_pass = ttk.Entry(frame, show="*")
    entry_pass.pack(fill="x", pady=5)

    def guardar():
        if entry_user.get() == "user1" and entry_pass.get() == "pass1":
            ventana.destroy()
            on_success()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    ttk.Button(frame, text="Guardar", command=guardar).pack(pady=10)


# ---------------- VENTANA ID INFO ----------------
def abrir_id_info(root, politica):
    ventana = tk.Toplevel(root)
    ventana.title(f"ID Info - {politica['politica']}")
    ventana.geometry("700x200")

    frame = ttk.Frame(ventana, padding=10)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Campo", font=("Arial", 10, "bold")).grid(row=0, column=0)
    ttk.Label(frame, text="Valor", font=("Arial", 10, "bold")).grid(row=0, column=1)
    ttk.Label(frame, text="ID", font=("Arial", 10, "bold")).grid(row=0, column=2)

    campos = ["politica", "tipo de politica"]

    for row, campo in enumerate(campos, start=1):
        ttk.Label(frame, text=campo).grid(row=row, column=0, sticky="w")

        v = ttk.Entry(frame, width=30)
        v.insert(0, politica[campo])
        v.state(["readonly"])
        v.grid(row=row, column=1)

        i = ttk.Entry(frame, width=35)
        i.insert(0, politica["ids"][campo])
        i.state(["readonly"])
        i.grid(row=row, column=2)


# ---------------- VENTANA EDITAR ----------------
def abrir_editar(root, politica, labels):
    ventana = tk.Toplevel(root)
    ventana.title(f"Editar política - {politica['politica']}")
    ventana.geometry("650x300")

    frame = ttk.Frame(ventana, padding=10)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Campo", font=("Arial", 10, "bold")).grid(row=0, column=0)
    ttk.Label(frame, text="Valor actual", font=("Arial", 10, "bold")).grid(row=0, column=1)
    ttk.Label(frame, text="Nuevo valor", font=("Arial", 10, "bold")).grid(row=0, column=2)

    campos = [
        "politica",
        "descripcion",
        "tipo de politica",
        "contratos asociados"
    ]

    entradas = {}

    for row, campo in enumerate(campos, start=1):
        ttk.Label(frame, text=campo).grid(row=row, column=0, sticky="w")

        actual = ttk.Entry(frame, width=30)
        actual.insert(0, politica[campo])
        actual.state(["readonly"])
        actual.grid(row=row, column=1)

        nuevo = ttk.Entry(frame, width=30)
        nuevo.insert(0, politica[campo])
        nuevo.grid(row=row, column=2)

        entradas[campo] = nuevo

    def aplicar_cambios():
        for campo in campos:
            politica[campo] = entradas[campo].get()
            labels[campo].config(text=politica[campo])
        ventana.destroy()

    def guardar():
        pedir_credenciales(root, aplicar_cambios)

    ttk.Button(frame, text="💾 Guardar", command=guardar).grid(
        row=len(campos) + 1, column=2, pady=15, sticky="e"
    )


# ---------------- VENTANA PRINCIPAL ----------------
root = tk.Tk()
root.title("Políticas DS4MOVEUS")
root.geometry("1200x320")

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

headers = [
    "Política", "Descripción", "Tipo de política",
    "Contratos asociados", "ID Info", "Editar"
]

for col, h in enumerate(headers):
    ttk.Label(main_frame, text=h, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=8)


# ---------------- DATOS ----------------
politicas = [
    {
        "politica": "Restricción por conector",
        "descripcion": "Política accesible para conector 1",
        "tipo de politica": "Restricción Conector",
        "contratos asociados": "3",
        "ids": {
            "politica": "pol-con-948dj",
            "tipo de politica": "tipo-con-001x"
        }
    },
    {
        "politica": "Franja temporal",
        "descripcion": "Política accesible hasta 30/03",
        "tipo de politica": "Franja temporal",
        "contratos asociados": "4",
        "ids": {
            "politica": "pol-time-221sd",
            "tipo de politica": "tipo-time-332m"
        }
    }
]


# ---------------- FILAS ----------------
for row, politica in enumerate(politicas, start=1):
    labels = {}

    campos_visibles = [
        "politica",
        "descripcion",
        "tipo de politica",
        "contratos asociados"
    ]

    for col, campo in enumerate(campos_visibles):
        lbl = ttk.Label(main_frame, text=politica[campo])
        lbl.grid(row=row, column=col, padx=8, sticky="w")
        labels[campo] = lbl

    ttk.Button(
        main_frame,
        text="id_info",
        command=lambda p=politica: abrir_id_info(root, p)
    ).grid(row=row, column=4)


    ttk.Button(
        main_frame,
        text="✏️",
        command=lambda p=politica, l=labels: abrir_editar(root, p, l)
    ).grid(row=row, column=5)


root.mainloop()
