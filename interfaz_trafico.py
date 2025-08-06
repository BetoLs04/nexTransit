import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Ruta base (ajusta si estás en otra ubicación)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Funciones para ejecutar los scripts
def iniciar_deteccion():
    try:
        subprocess.Popen(["python", os.path.join(BASE_DIR, "detectar_autos.py")])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar la detección: {e}")

def iniciar_semaforo():
    try:
        subprocess.Popen(["python", os.path.join(BASE_DIR, "simulador_semaforo.py")])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar el semáforo: {e}")

def salir():
    ventana.destroy()

# Crear ventana
ventana = tk.Tk()
ventana.title("Control de Tráfico Inteligente")
ventana.geometry("500x400")
ventana.configure(bg="#1e1e1e")

# Título
titulo = tk.Label(
    ventana,
    text="🚦 Sistema de Tráfico Inteligente",
    font=("Helvetica", 20, "bold"),
    bg="#1e1e1e",
    fg="white"
)
titulo.pack(pady=20)

# Botón para detección de autos
btn_deteccion = tk.Button(
    ventana,
    text="🟢 Iniciar Detección de Autos",
    font=("Helvetica", 14),
    bg="#28a745",
    fg="white",
    width=30,
    height=2,
    command=iniciar_deteccion
)
btn_deteccion.pack(pady=10)

# Botón para simulación de semáforo
btn_semaforo = tk.Button(
    ventana,
    text="🔴 Iniciar Simulación de Semáforo",
    font=("Helvetica", 14),
    bg="#dc3545",
    fg="white",
    width=30,
    height=2,
    command=iniciar_semaforo
)
btn_semaforo.pack(pady=10)

# Botón para salir
btn_salir = tk.Button(
    ventana,
    text="⚪ Salir",
    font=("Helvetica", 12),
    bg="#6c757d",
    fg="white",
    width=20,
    height=1,
    command=salir
)
btn_salir.pack(pady=30)

# Iniciar ventana
ventana.mainloop()
