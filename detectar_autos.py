import cv2
import tkinter as tk
from tkinter import Button
from ultralytics import YOLO
from PIL import Image, ImageTk

# Modelo YOLO
modelo = YOLO("yolov8n.pt")

# Captura de cámara
camara = cv2.VideoCapture(0)

# Variables globales
zona_inicio = None
zona_fin = None
dibujando = False
zona_definida = False

limite_vehiculos = 5
clases_validas = ['car', 'truck', 'bus', 'motorcycle']
archivo_señal = "prioridad.txt"

# Crear ventana principal
root = tk.Tk()
root.title("Monitoreo de Tráfico")

# Frame para video
label_video = tk.Label(root)
label_video.pack()

# Canvas overlay para zona
canvas = tk.Canvas(label_video, width=800, height=600, highlightthickness=0)
canvas.place(x=0, y=0)

# Eventos del mouse para definir zona
def mouse_down(event):
    global zona_inicio, zona_fin, dibujando, zona_definida
    zona_inicio = (event.x, event.y)
    zona_fin = None
    dibujando = True
    zona_definida = False

def mouse_move(event):
    global zona_fin
    if dibujando:
        zona_fin = (event.x, event.y)

def mouse_up(event):
    global zona_fin, dibujando, zona_definida
    zona_fin = (event.x, event.y)
    dibujando = False
    zona_definida = True

canvas.bind("<Button-1>", mouse_down)
canvas.bind("<B1-Motion>", mouse_move)
canvas.bind("<ButtonRelease-1>", mouse_up)

# Función para reiniciar zona
def reset_zona():
    global zona_inicio, zona_fin, zona_definida
    zona_inicio = None
    zona_fin = None
    zona_definida = False

# Botones
btn_reset = Button(root, text="Reiniciar Zona", command=reset_zona)
btn_reset.pack(side=tk.LEFT, padx=10, pady=10)

btn_salir = Button(root, text="Salir", command=lambda: root.destroy())
btn_salir.pack(side=tk.RIGHT, padx=10, pady=10)

# Función para actualizar video en Tkinter
def actualizar_frame():
    global zona_inicio, zona_fin, zona_definida

    ret, frame = camara.read()
    if not ret:
        root.after(10, actualizar_frame)
        return

    frame = cv2.resize(frame, (800, 600))
    contador = 0

    # Si hay una zona dibujada (aunque no esté confirmada)
    if zona_inicio and zona_fin:
        x1, y1 = min(zona_inicio[0], zona_fin[0]), min(zona_inicio[1], zona_fin[1])
        x2, y2 = max(zona_inicio[0], zona_fin[0]), max(zona_inicio[1], zona_fin[1])

        # Crear overlay con relleno semitransparente
        overlay = frame.copy()
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (255, 0, 0), -1)  # Azul relleno
        alpha = 0.3  # Transparencia (0.0 = invisible, 1.0 = opaco)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        # Borde azul
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Texto "Zona de control"
        cv2.putText(frame, "Zona de control", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Procesar detección si zona está definida
    if zona_definida and zona_inicio and zona_fin:
        x1, y1 = min(zona_inicio[0], zona_fin[0]), min(zona_inicio[1], zona_fin[1])
        x2, y2 = max(zona_inicio[0], zona_fin[0]), max(zona_inicio[1], zona_fin[1])

        resultados = modelo(frame, verbose=False)[0]

        for box in resultados.boxes:
            cls_id = int(box.cls[0])
            nombre_clase = modelo.names[cls_id]
            conf = float(box.conf[0])
            xA, yA, xB, yB = map(int, box.xyxy[0])
            cx, cy = (xA + xB) // 2, (yA + yB) // 2

            if nombre_clase in clases_validas and conf > 0.5:
                if x1 < cx < x2 and y1 < cy < y2:
                    contador += 1
                    cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

        cv2.putText(frame, f"Vehiculos en zona: {contador}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        with open(archivo_señal, "w") as f:
            f.write("PRIORIDAD" if contador >= limite_vehiculos else "NORMAL")

    # Convertir frame a imagen para Tkinter
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)

    # Mostrar en label
    label_video.imgtk = imgtk
    label_video.configure(image=imgtk)

    root.after(10, actualizar_frame)

# Iniciar actualización
actualizar_frame()

# Ejecutar Tkinter
root.mainloop()

# Liberar recursos
camara.release()
cv2.destroyAllWindows()
