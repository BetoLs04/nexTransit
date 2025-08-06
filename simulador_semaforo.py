import cv2
import time
import os
import numpy as np

archivo_señal = "prioridad.txt"

estado_semaforo = "rojo"
ultimo_cambio = time.time()
tiempo_verde = 5
esperando_prioridad = False

while True:
    frame = 255 * np.ones((400, 300, 3), dtype=np.uint8)

    # Leer archivo de señal
    if os.path.exists(archivo_señal):
        with open(archivo_señal, "r") as f:
            señal = f.read().strip()
    else:
        señal = "NORMAL"

    tiempo_actual = time.time()

    # Manejo del estado del semáforo
    if estado_semaforo == "rojo" and señal == "PRIORIDAD":
        estado_semaforo = "verde"
        ultimo_cambio = tiempo_actual
    elif estado_semaforo == "verde":
        if tiempo_actual - ultimo_cambio >= tiempo_verde:
            estado_semaforo = "rojo"

    # Dibujar semáforo
    cv2.rectangle(frame, (100, 50), (200, 250), (50, 50, 50), -1)
    color_rojo = (0, 0, 255) if estado_semaforo == "rojo" else (50, 50, 50)
    color_verde = (0, 255, 0) if estado_semaforo == "verde" else (50, 50, 50)
    cv2.circle(frame, (150, 100), 30, color_rojo, -1)
    cv2.circle(frame, (150, 200), 30, color_verde, -1)
    cv2.putText(frame, f"Semaforo: {estado_semaforo.upper()}", (50, 300),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_verde if estado_semaforo == "verde" else color_rojo, 2)

    cv2.imshow("Simulador de Semáforo", frame)

    if cv2.waitKey(500) & 0xFF == 27:
        break
