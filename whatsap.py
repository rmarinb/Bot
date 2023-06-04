
"""
Este es un módulo que obtiene los datos para el envio del whatsap y lo manda
"""
import datetime
import pywhatkit as pw


def envio_mensaje(usuario, con):

    # Lo primero es obtener los datos necesarios para el envio del whatsap -> telefono del tutor del paciente    

    # Crear un cursor para ejecutar consultas
    cursor = con.cursor()

    # Conseguimos el máximo id_log
    cursor.execute("SELECT	u2.telefono, u2.nombre, u.nombre FROM usuarios u,usuarios u2 WHERE u.id = 1 AND u.id_tutor = u2.id;")
                   
    # Obtener el resultado de la consulta
    resul = cursor.fetchone()
    telefono = resul[0]
    nombre = resul[1]
    paciente = resul[2]
    cursor.close()
    
    # Una vez que tenemos el teléfono del tutor, hay que proceder a mandar el whatsap
    phone_number = "+34" + telefono  
    message = "Hola " + nombre + ", " + paciente + " no se ha tomado la medicación." 

    # Se manda el whatsap en el momento
    pw.sendwhatmsg_instantly (phone_number, message)
