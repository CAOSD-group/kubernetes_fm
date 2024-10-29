# Script to simplify and adapt a feature model for compatibility with Flamapy
# (also removes constraints)

import re

fm_original = 'variability_model/KubernetesFM.uvl'
fm_simplified = 'variability_model/KubernetesFM_simple.uvl'

# Palabras o caracteres a eliminar (comentar las que no se deseen eliminar)
words_to_delete = ['String ', 'Integer ', 'Boolean ', 'cardinality', '[1..*]']  
#words_to_delete = [] 

# Caracteres a eliminar de las restricciones (comentar los que no se deseen eliminar)
characters_to_delete = [' < ', ' > ', ' <=> ', ' == ', '//']
#characters_to_delete = ['//']

# Función para simplificar las restricciones
def simplified_constraints(restrictions):
    # Eliminar las restricciones no soportadas actualmente por Flamapy
    lines_restrictions = restrictions.split('\n')
    simplified_restrictions = []
    for line in lines_restrictions:
        if any(c in line for c in characters_to_delete):
            continue
        else:
            simplified_restrictions.append(line)
    return simplified_restrictions

# Función para procesar el texto
def generate_fm_simplified(fm_original, fm_simplified, palabras_a_eliminar):
    # Leer el archivo original
    with open(fm_original, 'r', encoding='utf-8') as f:
        text = f.read()

    # Eliminar y reemplazar las palabras o caracteres especificados
    for palabra in palabras_a_eliminar:
        text = text.replace(palabra, '')
    
    # Reemplazar todos los puntos por guiones bajos
    text = text.replace('.', '_')

    # Reemplazar '[1__*]' por '[1..*]'
    text = text.replace('[1__*]', '[1..*]')
    
    # Separar el modelo de características en dos partes: las características y las restricciones
    tree = re.split(r'^\s*constraints', text, maxsplit=1, flags=re.MULTILINE)[0]
    restrictions = re.split(r'^\s*constraints', text, maxsplit=1, flags=re.MULTILINE)[1]

    # Simplificar las restricciones (Comentar esta línea si no se desea simplificar las restricciones)
    restrictions = simplified_constraints(restrictions)
    

    # Guardar el texto modificado en un nuevo archivo
    with open(fm_simplified, 'w', encoding='utf-8') as f:
        f.write(tree)
        f.write('constraints')
        for i, line in enumerate(restrictions):
            f.write(line)
            if i < len(restrictions) - 1:
                f.write('\n')

# Llamar a la función para procesar el archivo
generate_fm_simplified(fm_original, fm_simplified, words_to_delete)

print(f"The processed file has been saved as {fm_simplified}")
