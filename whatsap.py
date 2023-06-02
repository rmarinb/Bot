
"""
Este es un módulo que obtiene los datos para el envio del whatsap y lo manda
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def envio_mensaje(usuario, con):

    # Lo primero es obtener los datos necesarios para el envio del whatsap -> telefono del tutor del paciente    

    # Crear un cursor para ejecutar consultas
    cursor = con.cursor()

    # Conseguimos el máximo id_log
    cursor.execute("SELECT	u2.telefono, u2.nombre FROM usuarios u,usuarios u2 WHERE u.id = 1 AND u.id_tutor = u2.id;")
                   
    # Obtener el resultado de la consulta
    resul = cursor.fetchone()
    telefono = resul[0]
    nombre = resul[1]
    cursor.close()
    
    # Una vez que tenemos el teléfono del tutor, hay que proceder a mandar el whatsap

    # Ruta al controlador descargado
    driver_path = 'D:/GDRIVE/Personal/UNIR/TFG/06_Codigo/Bot/Controlador/chromedriver.exe'

    # Configuración del controlador
    options = webdriver.ChromeOptions()
    #options.add_argument('--user-data-dir=C:\\Users\\tu_usuario\\AppData\\Local\\Google\\Chrome\\User Data')  # Ruta a tu perfil de Chrome
    options.add_argument('--user-data-dir=C:\\Users\\rmari\\AppData\\Local\\Google\\Chrome\\User Data')

    # Inicializar el controlador
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

    # Nombre o número de teléfono del contacto al que deseas enviar el mensaje
    # contacto = nombre
    contacto = 'Fer'

    mensaje = '¡Hola! Este es un mensaje enviado automáticamente desde Python. Una prueba de mi proyecto'

    # Buscar el campo de búsqueda
    search_field = driver.find_element_by_xpath('//input[@title="Buscar o empezar un chat"]')
    search_field.send_keys(contacto)
    search_field.send_keys(Keys.ENTER)

    # Esperar un poco para cargar el chat
    driver.implicitly_wait(5)

    # Encontrar el campo de mensaje y enviar el mensaje
    message_box = driver.find_element_by_xpath('//div[@class="_13mgZ"][@contenteditable="true"]')
    message_box.send_keys(mensaje)
    message_box.send_keys(Keys.ENTER)


