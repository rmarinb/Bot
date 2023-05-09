"""
Este es un módulo que proporciona conexión a la bbdd, lectura de los datos y llamada al teléfono
"""

import  datetime
import  mysql.connector
import  speech_recognition as sr
from twilio.rest import  Client

# Obtener la hora actual en formato personalizado
hora_actual = datetime.datetime.now().strftime("%H:%M")
hora_actual = '10:30'

# Imprimir la hora actual en formato personalizado
print("La hora actual en formato personalizado es:", hora_actual)

# Configuración de la conexión a la base de datos

config = {
    'user': 'root2',
    'password': 'root',
    'host': 'localhost',
    'database': 'crudnodejs'
}


"""
Este es un módulo que transcribe el audio de la llamada  
"""
def transcribir_audio(audio):
    
    # Crear un objeto reconocedor
    recognizer = sr.Recognizer()

    # Especificar la ubicación del archivo WAV a transcribir
    archivo_wav = "ruta_del_archivo.wav"

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
            print("Error en la solicitud al servicio de reconocimiento de voz: ", str(e))

    return 1

"""
Metodo para realizar la llamada
"""

def llamada(medicamento, cantidad, telefono):          
   

    # Establece las variables necesarias para realizar la llamada    
    account_sid = "AC58c72fb9cc90d1aed4c8f618d5c42b2e"
    auth_token = "bf90502fa03b42bc6eb3b1b4d8e240e0"
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        twiml='<Response><Say>Hola, esta es una llamada de prueba de Twilio de Rosana.</Say></Response>',
        url="http://demo.twilio.com/docs/voice.xml",
        to="+34616716269",
        from_="+13204094105"
    )

    print(call.sid)

    # Obtener el enlace al archivo de grabación de la llamada
    recording_url = call.recording_url

    # Descargar y guardar el archivo de grabación
    recording = client.recordings(call.recording_sid).fetch()
    recording_content = recording.content
    with open('grabacion.wav', 'wb') as f:
        f.write(recording_content)

    # Transcribimos la llamada realizada a un texto
    transcribir_audio(f)

    return 1

"""
Metodo para realizar la búsqueda de los datos de la medicación y luego llamar
"""
def datos_hora(hora):
    print("Las dos horas son IGUALES")
    print(hora)
    hora='10:30'

    # Conexión a la base de datos
    cnx = mysql.connector.connect(**config)

    cursor = cnx.cursor()
          
    cursor.execute("SELECT m.Nombre_Comun, Cantidad, Telefono FROM crudnodejs.dosis d, crudnodejs.medicamentos m, crudnodejs.usuarios u WHERE d.ID_Medicamento = m.ID_Medicamento AND u.ID = 1 AND u.ID = d.ID_Usuario AND Hora = %s", (hora,))
                   
    # Obtener el resultado de la consulta
    medicamento = cursor.fetchone()
    # Imprimir el resultado
    print(medicamento[0])
    print(medicamento[1])
    print(medicamento[2])

    # llamada(medicamento[0], medicamento[1], medicamento[2])
    return 1

# Conexión a la base de datos
cnx = mysql.connector.connect(**config)

# Realización de una consulta a la base de datos
cursor = cnx.cursor()
query = "SELECT Hora FROM dosis WHERE ID_Usuario = 1"
cursor.execute(query)

# Recuperación de los resultados de la consulta
for resultado in cursor:

    # print("La hora de la tabla es:" , resultado)
    
    # Convertimos la tupla en el mismo formato que la hora actual 
    hora_resultado = datetime.datetime.strptime(resultado[0], "%H:%M").time()
    hora_resultado2 = hora_resultado.strftime("%H:%M")

    # Imprimir la hora como objeto datetime.time
    print("La hora como objeto datetime.time es:", hora_resultado2)

    if hora_resultado2 == hora_actual:        
        datos_hora(hora_actual)
    
# Cierre de la conexión
cursor.close()
cnx.close()
