import cv2
import numpy as np 
import pyautogui
import keyboard

# Configuración de la grabación
fps = 10.0 
resolucion = pyautogui.size()
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Verificar si se puede crear el escritor de video
if not cv2.VideoWriter_fourcc(*'mp4v'):
    print("No se pudo crear el escritor de video")
    exit()

# Crear el escritor de video
out = cv2.VideoWriter('grabacion.mp4', fourcc, fps, resolucion)

# Iniciar la grabación
while True:
    try:
        # Capturar la pantalla
        frame = np.array(pyautogui.screenshot())

        # Verificar si el frame es válido
        if frame is not None and frame.any():
            # Convertir el frame a BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Escribir el frame en el video
            out.write(frame)

        # Verificar si se presionó la tecla 'q'
        if keyboard.is_pressed('q'):
            break

    except Exception as e:
        # Manejar cualquier error que surja durante la captura o escritura de la pantalla
        print(f"Error: {e}")

# Liberar el escritor de video
out.release()
cv2.destroyAllWindows()

