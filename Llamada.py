import  speech_recognition as sr
from    twilio.rest import  Client
from twilio.rest.resources import Call
import  time

"""
Este es un módulo que llama por TELEFONO
"""

"""
Este es un módulo que transcribe el audio de la llamada a una variable texto_transcrito  
"""
def transcribir_audio(audio):
    
    print('Entra en transcribir audio. Con el audio en el parámetro.')

    # Crear un objeto reconocedor
    recognizer = sr.Recognizer()

    # Especificar la ubicación del archivo WAV a transcribir
    archivo_wav = audio

    print('Tenemos el nombre y la ubicacion del archivo')

    # Abrir el archivo WAV
    with sr.AudioFile(archivo_wav) as source:
        # Leer el audio del archivo
        audio = recognizer.record(source)

        try:
            # Realizar la transcripción utilizando el servicio de reconocimiento de voz de Google
            texto_transcrito = recognizer.recognize_google(audio, language="es")

            # Imprimir el texto transcrito
            print("Texto transcrito: ", texto_transcrito)
        except sr.UnknownValueError:
            print("No se pudo transcribir el audio")
        except sr.RequestError as e:
            print("Error en la solicitud al servicio de reconocimiento de voz:   ", str(e))

    print('Termina el transcribir')

    return 1

"""
Metodo para realizar la llamada
"""

def llamar(medicamento, cantidad, telefono):          
   
    print('Entra en llamada')

    # Establece las variables necesarias para realizar la llamada    
    account_sid = "AC58c72fb9cc90d1aed4c8f618d5c42b2e"
    auth_token = "bf90502fa03b42bc6eb3b1b4d8e240e0"
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        twiml='<Response><Say>Hola, ¿se ha tomado el ' + medicamento + '? .</Say></Response>',        
        to="+34616716269",
        from_="+13204094105"
    )

    print('Esta llamando. Identificador:', call.sid)

    # Hasta que el usuario cuelgue, vamos a ir comprobando el estado, para luego procesar el audio.
    cont=0
    
    while True:

        # Si estamos mucho rato que se salga
        cont+=1
        print(cont)

        if cont > 100:
            break
        
        time.sleep(0.5)    
    
        if call.status == 'completed':
            print("La llamada ha finalizado")
            recordings = call.recordings.list()
            if len(recordings) > 0:
                recording_url = recordings[0].uri
                print("URL del archivo de audio:", recording_url)

                # Obtener el enlace al archivo de grabación de la llamada
                recording_url = call.recording_url
                
                # Descargar y guardar el archivo de grabación
                recording = client.recordings(call.recording_sid).fetch()
                recording_content = recording.content
                with open('grabacion.wav', 'wb') as f:
                    f.write(recording_content)
                print('Descargada la llamada en ', recording_content)

                return recording_content
            else: 
                print("No hay grabación de la llamada")
                return  -1
        elif call.status == 'in-progress':
                print("La llamada está en progreso.")
        elif call.status == 'queued':
                print("La llamada está en cola.")
        else:
            print("La llamada ha fallado o sido cancelada") 

    return -1
