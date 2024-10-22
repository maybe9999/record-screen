import cv2          #Procesamiento de img y videos
import numpy as np  #crear vectores y matrices grandes multidimensionales, Funciones matemáticas de alto nivel
import pyautogui    #Interactuar mouse y teclado, captura de pantalla.
import keyboard     #Control del teclado.

# Configuración de la grabación
fps = 10.0 
resolucion = pyautogui.size()
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
valor_de_estado = 0
letra = ""

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
        if valor_de_estado == 1:
            valor_de_estado = 2
        # Verificar si el frame es válido
        if frame is not None and frame.any() and letra == "c":
            # Convertir el frame a BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Escribir el frame en el video
            out.write(frame)
            if valor_de_estado < 1:
                print("Grabando...")
                valor_de_estado = 1
        # Verificar si se presionó la tecla 'q'
        if keyboard.is_pressed('q'):
            print("grabacion detenida")
            break
        if keyboard.is_pressed('c'):
            letra = "c"
            print("empezando grabacion")

    except Exception as e:
        # Manejar cualquier error que surja durante la captura o escritura de la pantalla
        print(f"Error: {e}")

# Liberar el escritor de video
out.release()
cv2.destroyAllWindows()