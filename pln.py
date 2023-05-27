"""
Este es un módulo que procesa el texto trascrito e intenta determinar qué ha dicho el paciente 
"""

def procesa_pln(texto):

    # Primero convertimos el diccionario en textos independientes en los que vamos a buscar un 'SI'
    for valor in texto.items():
        print("El valor es:", valor)    

    var = ('alternative', [{'transcript': 'el ibuprofeno', 'confidence': 0.96330917}, {'transcript': 'ibuprofeno'}, {'transcript': 'el ibuprofeno si'}, {'transcript': 'el ibuprofeno sí'}])

    segundo_elemento = var[1]
    print(segundo_elemento)
    # [{'transcript': 'el ibuprofeno', 'confidence': 0.96330917},
    #  {'transcript': 'ibuprofeno'},
    #  {'transcript': 'el ibuprofeno si'},
    #  {'transcript': 'el ibuprofeno sí'}]

    mi_variable = "1234567890"

    ultimos_cinco_digitos = mi_variable[-5:]

    print(ultimos_cinco_digitos)  # Imprime "56789"

    print("esta es mi lista")
    for txt in segundo_elemento:
        print(txt)
        txt_recortado = txt[-5]
        print("los ultimos cinco digitos son: ", txt_recortado)

    return  1
