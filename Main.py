"""
Este es un módulo PRINCIPAL que proporciona conexión a la bbdd y lectura de los datos 
"""

import  datetime
import  mysql.connector
import  Llamada as c

# Obtener la hora actual en formato personalizado
hora_actual = datetime.datetime.now().strftime("%H:%M")
hora_actual = '10:30'

# Imprimir la hora actual en formato personalizado
print("La hora actual en formato personalizado es:", hora_actual)

# Configuración de la conexión a la base de datos
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'crudnodejs'
}

"""
Metodo para realizar la búsqueda de los datos de la medicación 
"""
def principal(hora):
    
    print("Las dos horas son IGUALES")
    print(hora)
    hora='10:30'

    # Conexión a la base de datos para obtener los datos de la prescripción
    cnx = mysql.connector.connect(**config)

    cursor = cnx.cursor()          
    cursor.execute("SELECT m.Nombre_Comun, Cantidad, Telefono FROM crudnodejs.dosis d, crudnodejs.medicamentos m, crudnodejs.usuarios u WHERE d.ID_Medicamento = m.ID_Medicamento AND u.ID = 1 AND u.ID = d.ID_Usuario AND Hora = %s", (hora,))
                   
    # Obtener el resultado de la consulta
    medicamento = cursor.fetchone()
    # Imprimir el resultado
    print(medicamento[0])
    print(medicamento[1])
    print(medicamento[2])

    # Realizamos la llamada
    resul = c.llamar(medicamento[0], medicamento[1], medicamento[2])

    if resul == 1:
        print("La llamada se ha realizado correctamente")        
    else:
        print("Ha habido un error realizando  la llamada")
        return -1

    # Transcribimos la llamada realizada a un texto
    resul = c.transcribir_audio(f)

    if resul == 1:
        print("La llamada se ha transcrito correctamente")              
    else:
        print("Ha habido un error transcribiendo la llamada")
        return -1

    return 1

# **************************************************************************************************************************************
# EJECUCION PRINCIPAL ******************************************************************************************************************
# Conexión a la base de datos

cnx = mysql.connector.connect(**config)

# Realización de una consulta a la base de datos
cursor = cnx.cursor()
query = "SELECT Hora FROM dosis WHERE ID_Usuario = 1"
cursor.execute(query)

# Recuperación de los resultados de la consulta
for resultado in cursor:
       
    # Convertimos la tupla en el mismo formato que la hora actual 
    hora_resultado = datetime.datetime.strptime(resultado[0], "%H:%M").time()
    hora_resultado2 = hora_resultado.strftime("%H:%M")

    # Imprimir la hora como objeto datetime.time
    print("La hora como objeto datetime.time es:", hora_resultado2)

    if hora_resultado2 == hora_actual:        
        principal(hora_actual)
    else:
        print("No ha dosis a la hora ", hora_actual)
    
# Cierre de la conexión de base de datos
cursor.close()
cnx.close()
