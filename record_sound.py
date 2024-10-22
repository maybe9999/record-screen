import pyaudio
import wave

# Configuraciones
FORMAT = pyaudio.paInt16  # Formato de audio
CHANNELS = 1              # Número de canales (1 para mono, 2 para estéreo)
RATE = 44100              # Frecuencia de muestreo
CHUNK = 1024              # Tamaño del buffer
RECORD_SECONDS = 10       # Duración de la grabación
DEVICE = 1
WAVE_OUTPUT_FILENAME = "output.wav"  # Archivo de salida

p = pyaudio.PyAudio()

# Abre el flujo de audio
stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,  # Modo de entrada
                    #input_device_index=DEVICE,
                    frames_per_buffer=CHUNK)

print("Grabando...")


for a in range(p.get_device_count()):
    print("prueba",str(p.get_device_info_by_index(a)).replace(",", "\n"))

frames = []

for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Grabación terminada.")

# Detener y cerrar el flujo
stream.close()
p.terminate()


# Guardar la grabación en un archivo WAV
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Grabación guardada como {WAVE_OUTPUT_FILENAME}")
