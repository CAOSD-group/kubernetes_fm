# Script that counts and groups invalid configurations by 'ObjectType' in a CSV file and saves the result in a text file.
# Useful for identifying which ones are failing and which to implement next.
# The functionality to count valid configurations by 'ObjectType' and save the result in a text file has been added.

import pandas as pd

# Cargar el archivo en un dataframe
df = pd.read_csv('NonValidConfigs.csv')

# Contar las veces que aparece cada elemento en la columna 'ObjectType'
object_type_counts = df['ObjectType'].value_counts()

# Ordenar de mayor a menor (value_counts ya devuelve el resultado ordenado)
object_type_counts_sorted = object_type_counts.sort_values(ascending=False)

# Guardar el resultado en un archivo de texto
with open('failed_objects.txt', 'w') as f:
    f.write(object_type_counts_sorted.to_string())

# Cargar el archivo en un dataframe
df = pd.read_csv(r'configurations/Configurations.csv')

# Contar las veces que aparece cada elemento en la columna 'ObjectType'
object_type_counts = df['ObjectType'].value_counts()

# Ordenar de mayor a menor (value_counts ya devuelve el resultado ordenado)
object_type_counts_sorted = object_type_counts.sort_values(ascending=False)

# Guardar el resultado en un archivo de texto
with open('objects.txt', 'w') as f:
    f.write(object_type_counts_sorted.to_string())
