# Script que cuenta y agrupa las configuraciones no válidas por 'ObjectType' en un archivo CSV y guarda el resultado en un archivo de texto.
# útil para saber cuales estan fallando y cuales implementar a continuación.
# Se ha añadido la funcionalidad de contar las configuraciones válidas por 'ObjectType' y guardar el resultado en un archivo de texto.

import pandas as pd

# Cargar el archivo en un dataframe
df = pd.read_csv('configsNoValidas.csv')

# Contar las veces que aparece cada elemento en la columna 'ObjectType'
object_type_counts = df['ObjectType'].value_counts()

# Ordenar de mayor a menor (value_counts ya devuelve el resultado ordenado)
object_type_counts_sorted = object_type_counts.sort_values(ascending=False)

# Guardar el resultado en un archivo de texto
with open('objetos_fallidos.txt', 'w') as f:
    f.write(object_type_counts_sorted.to_string())

# Cargar el archivo en un dataframe
df = pd.read_csv(r'C:\Users\CAOSD\Documents\githubScraping\Configuraciones.csv')

# Contar las veces que aparece cada elemento en la columna 'ObjectType'
object_type_counts = df['ObjectType'].value_counts()

# Ordenar de mayor a menor (value_counts ya devuelve el resultado ordenado)
object_type_counts_sorted = object_type_counts.sort_values(ascending=False)

# Guardar el resultado en un archivo de texto
with open('objetos.txt', 'w') as f:
    f.write(object_type_counts_sorted.to_string())
