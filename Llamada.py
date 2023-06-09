import  time
import  requests
import  speech_recognition as sr
from    twilio.rest import  Client
from    pydub import AudioSegment

"""
Este es un módulo que llama por TELEFONO y TRANSCRIBE LA LLAMADA
"""

def transcribir_audio(audio_completo):
    
    # primero dividimos el audio en cachitos pequeños y nos cogemos el último
    audio = AudioSegment.from_wav(audio_completo)

    # Definir la duración de cada segmento en milisegundos (por ejemplo, 10 segundos)
    segment_duration = 10000

    # Dividir el audio en segmentos más pequeños
    segments = [audio[i:i+segment_duration] for i in range(0, len(audio), segment_duration)]

    # Convertir el ultimo segmento a formato WAV en memoria
    segment = segments[1]
    segment_wav = segment.export(format="wav") 
    
    # Crear un objeto reconocedor
    recognizer = sr.Recognizer()   

    # Abrir el archivo WAV
    with sr.AudioFile(segment_wav) as source:
        # Leer el audio del archivo
        audio = recognizer.record(source)
        try:
            # Realizar la transcripción utilizando el servicio de reconocimiento de voz de Google
            texto_transcrito = recognizer.recognize_google(audio, show_all=True, language="es")            
            return texto_transcrito
        except sr.UnknownValueError:
            print("No se pudo transcribir el audio. Desconocemos el error. ")
            return -1 
        except sr.RequestError as erro:
            print("Error en la solicitud al servicio de reconocimiento de voz:   ", str(erro))
            return -1
      
    return 1
"""
Metodo para realizar la llamada
"""

def llamar(medicamento, cantidad, telefono):          

    tele = "+34" + telefono

    # Establece las variables necesarias para realizar la llamada 
    # Estos datos son propios de mi usuario de twilio    
    # Con estos datos no funciona, pues no son los reales: 
    account_sid = "1"
    auth_token = "1"

    client = Client(account_sid, auth_token)

    call = client.calls.create(
        twiml='<Response><Gather action="/process-response" method="POST" timeout="10"><Say language="es-ES">Hola, ¿se ha tomado el ' + medicamento + '? .</Say></Gather></Response>',
        to=tele,
        from_="+13204094105",   
        record=True
    )      
    
    # Hasta que el usuario cuelgue, vamos a ir comprobando el estado, para luego procesar el audio.
    cont=0
    
    while True:

        # Si estamos mucho rato que se salga
        cont+=1        

        if cont > 100:
            break
        
        time.sleep(0.5)   
        
        call_details = client.calls(call.sid).fetch()
        if call_details.status == 'completed' :
            calla = call.sid
                
            recordings = client.recordings.list(call_sid=calla)            
                    
            recording = recordings[0]
            recording_sid = recording.sid
            
            # Se monta la URL de donde se descarga 
            recording_url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Recordings/{recording_sid}.wav'
                    
            response = requests.get(recording_url, auth=(account_sid, auth_token))
            filename = f'{recording_sid}.wav'
            # Descargamos los archivos 
            with open(filename, 'wb') as file:
                file.write(response.content)        
            return filename              
        
        elif call_details.status == 'in-progress':
            print("La llamada está en progreso.")
        elif call_details.status == 'queued':
            print("La llamada está en cola.")
        else:
            print("La llamada ha fallado o sido cancelada") 
        
    return -1

