import cv2
import time
import os
import numpy as np

archivo_señal = "prioridad.txt"

estado_semaforo = "rojo"
ultimo_cambio = time.time()
tiempo_verde = 5

while True:
    # Fondo blanco
    frame = 255 * np.ones((400, 600, 3), dtype=np.uint8)

    # Leer archivo de señal
    if os.path.exists(archivo_señal):
        with open(archivo_señal, "r") as f:
            señal = f.read().strip()
    else:
        señal = "NORMAL"

    tiempo_actual = time.time()

    # Manejo del estado del semáforo 1
    if estado_semaforo == "rojo" and señal == "PRIORIDAD":
        estado_semaforo = "verde"
        ultimo_cambio = tiempo_actual
    elif estado_semaforo == "verde":
        if tiempo_actual - ultimo_cambio >= tiempo_verde:
            estado_semaforo = "rojo"

    # Semáforo 1
    cv2.rectangle(frame, (100, 50), (200, 250), (50, 50, 50), -1)
    color_rojo_1 = (0, 0, 255) if estado_semaforo == "rojo" else (50, 50, 50)
    color_verde_1 = (0, 255, 0) if estado_semaforo == "verde" else (50, 50, 50)
    cv2.circle(frame, (150, 100), 30, color_rojo_1, -1)
    cv2.circle(frame, (150, 200), 30, color_verde_1, -1)
    cv2.putText(frame, "CALLE 1", (100, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Semáforo 2 (opuesto)
    estado_semaforo_2 = "verde" if estado_semaforo == "rojo" else "rojo"
    cv2.rectangle(frame, (400, 50), (500, 250), (50, 50, 50), -1)
    color_rojo_2 = (0, 0, 255) if estado_semaforo_2 == "rojo" else (50, 50, 50)
    color_verde_2 = (0, 255, 0) if estado_semaforo_2 == "verde" else (50, 50, 50)
    cv2.circle(frame, (450, 100), 30, color_rojo_2, -1)
    cv2.circle(frame, (450, 200), 30, color_verde_2, -1)
    cv2.putText(frame, "CALLE 2", (400, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Texto estado
    cv2.putText(frame, f"Semaforo 1: {estado_semaforo.upper()}", (50, 300),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(frame, f"Semaforo 2: {estado_semaforo_2.upper()}", (350, 300),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Mostrar ventana
    cv2.imshow("Simulador de Semáforos", frame)

    if cv2.waitKey(500) & 0xFF == 27:
        break

cv2.destroyAllWindows()
