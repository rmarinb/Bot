"""
Este es un módulo PRINCIPAL que proporciona conexión a la bbdd y lectura de los datos 
"""

import  datetime
import  mysql.connector
import  Llamada as c
import  pln as p 
import  Log as l
import  whatsap as w

# Obtener la hora actual en formato personalizado
hora_actual = datetime.datetime.now().strftime("%H:%M")
hora_actual = '10:30' #forzamos la hora para pruebas

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

    # Conexión a la base de datos para obtener los datos de la prescripción
    cnx = mysql.connector.connect(**config)

    cursor = cnx.cursor()          
    cursor.execute("SELECT m.Nombre_Comun, Cantidad, Telefono, d.id_dosis FROM crudnodejs.dosis d, crudnodejs.medicamentos m, crudnodejs.usuarios u WHERE d.ID_Medicamento = m.ID_Medicamento AND u.ID = 1 AND u.ID = d.ID_Usuario AND Hora = %s", (hora,))
                   
    # Obtener el resultado de la consulta
    medicamento = cursor.fetchone()
    
    # Realizamos la llamada
    resul = c.llamar(medicamento[0], medicamento[1], medicamento[2])

    if resul == -1:
        print("Ha habido un error realizando  la llamada.")
        l.log("Error llamada", id_Dosis, usuario, cnx)
        return -1    
    
    # Transcribimos la llamada realizada a un texto    
    resul_escritura = c.transcribir_audio(resul)

    if resul_escritura == -1:
        print("Ha habido un error transcribiendo la llamada. Se desconoce el error")
        l.log("Error transc", id_Dosis, usuario, cnx)
        return -1

    #Como se ha transcrito la llamada, vamos a procesar el lenguaje natural buscando un afirmativo
    resul_pln = p.procesa_pln(resul_escritura);

    if resul_pln == -1:
        print("Ha habido un error en el PLN del texto de la trascripción.")
        l.log("Error proces", id_Dosis, usuario, cnx)
    elif resul_pln == 0:
        print("El paciente no se ha tomado la medicación.") 
        l.log("ERROR", medicamento[3], 1, cnx)
        w.envio_mensaje(1, cnx)
    elif resul_pln == 1:
        print("El paciente se ha tomado la medicacion.")
        l.log("OK", medicamento[3], 1, cnx)        
    
    return 1

# **************************************************************************************************************************************
# EJECUCION PRINCIPAL ******************************************************************************************************************
# Conexión a la base de datos

cnx = mysql.connector.connect(**config)

# Realización de una consulta a la base de datos
cursor = cnx.cursor()
query = "SELECT Hora, ID_Usuario, ID_dosis FROM dosis"
cursor.execute(query)

# Recuperación de los resultados de la consulta
for resultado in cursor:
       
    # Convertimos la tupla en el mismo formato que la hora actual 
    hora_resultado  = datetime.datetime.strptime(resultado[0], "%H:%M").time()
    hora_resultado2 = hora_resultado.strftime("%H:%M")
    usuario         = resultado[1]
    id_Dosis        = resultado[2]

    # Imprimir la hora como objeto datetime.time    
    if hora_resultado2 == hora_actual:        
        principal(hora_actual)
    
# Cierre de la conexión de base de datos
cursor.close()
cnx.close()
