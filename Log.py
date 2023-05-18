import  datetime

"""
Este es un módulo que guarda el LOG De las llamadas
"""

def log(resultado, dosis, usuario, cnx):

    hora_actual = datetime.datetime.now().strftime("%H:%M")

    # Crear un cursor para ejecutar consultas
    cursor = cnx.cursor()

    # Conseguimos el máximo id_log
    cursor.execute("SELECT max(ID_Log) FROM log")
                   
    # Obtener el resultado de la consulta
    id_log = cursor.fetchone()
    
    print("Log máximo que hay", id_log[0]) 
    clave = id_log[0] + 1

    # Sentencia SQL de inserción
    sql = "INSERT INTO logs (ID_Log, fecha, resultado, id_dosis, id_usuario) VALUES (%s, %s, %s, %s, %s)"

    # Valores a insertar
    valores = (clave, hora_actual, resultado, dosis, usuario)

    # Ejecutar la sentencia SQL con los valores
    cursor.execute(sql, valores)

    # Confirmar los cambios en la base de datos
    cnx.commit()

    # Cerrar el cursor y la conexión
    cursor.close()
