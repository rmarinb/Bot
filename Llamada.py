import  time
import requests
import  speech_recognition as sr
from    twilio.rest import  Client


"""
Este es un módulo que llama por TELEFONO y TRANSCRIBE LA LLAMADA
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
        except sr.RequestError as erro:
            print("Error en la solicitud al servicio de reconocimiento de voz:   ", str(erro))

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
        twiml='<Response><Gather action="/process-response" method="POST" timeout="10"><Say language="es-ES">Hola, ¿se ha tomado el ' + medicamento + '? .</Say></Gather></Response>',
        to="+34616716269",
        from_="+13204094105",   
        record=True
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

        call_details = client.calls(call.sid).fetch()        
        if call_details.status == 'completed':
       
            print("Se va a intentar descargar la llamada en un archivo de audio.") 
            
            recordings = client.recordings.list()

            for recording in recordings:
                recording_sid = recording.sid
                recording_url = recording.uri.replace('.json', '.mp3')
                response = client.request('GET', recording_url)
                with open(f'{recording_sid}.mp3', 'wb') as file:
                    file.write(response.content)

            return 1
        
        elif call_details.status == 'in-progress':
                print("La llamada está en progreso.")
        elif call_details.status == 'queued':
                print("La llamada está en cola.")
        else:
            print("La llamada ha fallado o sido cancelada") 

    return -1

