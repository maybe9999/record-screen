import pyaudio
import wave


defaultframes = 512

class textcolors:
    blue = '\033[94m'
    green = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    end = '\033[0m'

recorded_frames = []
device_info = {}
useloopback = False
recordtime = 5

#Use module
p = pyaudio.PyAudio()

#Set default to first in list or ask Windows  ---   Establecer como predeterminado el primero en la lista o preguntar a Windows
try:
    default_device_index = p.get_default_input_device_info() #Diccionario
    print("Dispositvo predeterminado: ", default_device_index)
except IOError:
    print("Excepción en Dispositivo predeterminado...")
    default_device_index = -1

#Select Device
print("Available devices:\n")
for i in range(0, p.get_device_count()): #Devuelve el numero de dispositivos de PortAudio host Apis
    info = p.get_device_info_by_index(i) #Itera a través de todos los dispositivos imprimiéndoles
    print(str(info["index"]) + ": \t %s \n \t %s \n" % (info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))

    if default_device_index == -1:
        default_device_index = info["index"]

#Handle no devices available
if default_device_index == -1:
    print("No device available. Quitting.")
    exit()


#Get input or default
device_id = int(input("Choose device ["+ str(default_device_index) + "]: ") or default_device_index)
print("")

#Get device info
try:
    device_info = p.get_device_info_by_index(device_id)
    print("Dispositivo elegido: ", device_info)
except IOError:
    device_info = p.get_device_info_by_index(default_device_index)
    print("Selection not available, using default.")

#Choose between loopback or standard mode
is_input = device_info["maxInputChannels"] > 0 #Tiene 1 canal de entrada o mas?
is_wasapi = (p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1
if is_input:
    print("Selection is input using standard mode.\n")
else:
    if is_wasapi:
        useloopback = True
        print("Selection is output. Using loopback mode.\n")
    else:
        print("Selection is output and does not support loopback mode. Quitting.\n")
        exit()

recordtime = int(input("Record time in seconds [" + str(recordtime) + "]: ") or recordtime)

#Open stream
channelcount = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
stream = p.open(format = pyaudio.paInt16,
                channels = channelcount,
                rate = int(device_info["defaultSampleRate"]),
                input = True,
                frames_per_buffer = defaultframes,
                input_device_index = device_info["index"],
                as_loopback = useloopback)

#Start Recording
print("Starting...")

for i in range(0, int(int(device_info["defaultSampleRate"]) / defaultframes * recordtime)):
    recorded_frames.append(stream.read(defaultframes))
    print(".")

print("End.")
#Stop Recording

stream.stop_stream()
stream.close()

#Close module
p.terminate()

filename = input("Save as [" + textcolors.blue + "out.wav" + textcolors.end + "]: ") or "out.wav"

waveFile = wave.open(filename, 'wb')
waveFile.setnchannels(channelcount)
waveFile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
waveFile.setframerate(int(device_info["defaultSampleRate"]))
waveFile.writeframes(b''.join(recorded_frames))
waveFile.close()

"""
Con p.get_host_api_info_by_index(0) se obtiene un diccionario con los parámetros / valores de ese HOST API que consultemos mediante su indice.


Hay distintos tipos de HostApi, por ejemplo: "MME", 'Windows DirectSound', "Windows WASAPI", "Windows WDM-KS". (Básicamente son controladores de audio de Windows)

- MMM: Entorno Multimedia de Microsoft. Controlador nativo de windows. Primer controlador de audio lanzado con windows 3.1. Muchas tarjetas de audio y software de audio es compatible con MME
- WASAPI: Windows Audio Session API. Controlador de audio reciente en windows. Permite enviar directamente audio a la salida de hardware con el Modo Exclusivo. Permite codificar audio envolvente para reproducir a través de las salidas de audio digital.
- WDM: Windows Driver Model. No es un controlador de audio. Permite a los controladores convertirse en parte del kernel de win. Es el estándar para la mayoría de las apps y juegos.
- DirectSound: Otro controlador de windows...



Los Host api están ligados a dispositivos, podemos saber a que Host Api esta ligado cada dispositivo
consultando el indice que este contiene de HostApi, por ejemplo:
p.get_device_info_by_index(10) = 
{'index': 10, 'structVersion': 2, 'name': 'Dolby (Realtek High Definition Audio)', 'hostApi': 2, 'maxInputChannels': 0,
'maxOutputChannels': 2, 'defaultLowInputLatency': 0.0, 'defaultLowOutputLatency': 0.003, 'defaultHighInputLatency': 0.0,
'defaultHighOutputLatency': 0.01, 'defaultSampleRate': 48000.0}

En el ejemplo anterior este dispositivo tiene un indice 2 de hostApi que pertenece a "Windows WASAPI":
p.get_host_api_info_by_index(2):
{'index': 2, 'structVersion': 1, 'type': 13, 'name': 'Windows WASAPI', 'deviceCount': 3, 'defaultInputDevice': 11, 'defaultOutputDevice': 10}

Lo que a nosotros nos interesa es un dispositivo que tenga canales de salida de audio y que el indice de hostApi 
coincida con el hostApi "Windows WASAPI".




"""