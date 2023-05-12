import  speech_recognition as sr
from    twilio.rest import  Client

"""
Este es un módulo que llama por TELEFONO
"""

"""
Este es un módulo que transcribe el audio de la llamada a una variable texto_transcrito  
"""
def transcribir_audio(audio):
    
    print('Entra en transcribir audio')

    # Crear un objeto reconocedor
    recognizer = sr.Recognizer()

    # Especificar la ubicación del archivo WAV a transcribir
    archivo_wav = "ruta_del_archivo.wav"

    print('Tenemos el nombre del archivo')

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
        # twiml='<Response><Say>Hola, ¿se ha tomado el ' + medicamento + '? .</Say></Response>',
        twiml='<Response><Say>Voz de la llamada de Rosana</Say></Response>',
        url="http://demo.twilio.com/docs/voice.xml",
        to="+34616716269",
        from_="+13204094105"
    )

    print('Esta llamando. Identificador:', call.sid)

    if call.status == 'completed':
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
            print('Descarga la llamada')
        else: 
            print("No hay grabación de la llamada")
            return  0

    else:
        print("La llamada no ha finalizado")
     
    return 1
