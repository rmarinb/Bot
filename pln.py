from unidecode import unidecode

"""
Este es un módulo que procesa el texto trascrito e intenta determinar qué ha dicho el paciente 
"""

def procesa_pln(texto):

    # cogemos la parte de texto alternativo, porque el principal no detecta lo último dicho 
    var = texto['alternative']         

    # de todas las transcripciones alternativas, me quedo con la última    
    tamano = len(var)   
    txt = var[tamano-1]

    # de la última me quedo con la parte transcrita
    texto = txt['transcript']
    
    # de la parte transcrita me quedo con los dos últimos caracteres    
    tamano = len(texto)
    txt = texto[-2:]
    
    # si el texto es un si, en mayusculas o minúsculas, con o sin acento
    if unidecode(txt.lower()) == "si":        
        return 1
    else:
        return 0

    return  -1
