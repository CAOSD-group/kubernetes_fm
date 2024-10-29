# Gets the number of valid, invalid, variability, and error configurations from a CSV file and saves the 
# configuration distribution based on the number of features in a CSV file. It also saves a CSV with the 
# failed configurations.

import csv
import pandas as pd

# Ruta del archivo CSV
ruta_csv = r'configurations/Configurations.csv'

# Leer el archivo CSV
df = pd.read_csv(ruta_csv)

# Contar las configuraciones válidas
configValidas = df[df['Valid'] == True].shape[0]

# Contar las configuraciones validas (sin variabilidad) que tienen cardinalidad 
configsValidasConCardinalidad = df[(df['Valid'] == True) & (df['ContainVariability'] == False) & (df['ContainCardinality'] == True)].shape[0]

# Contar las configuraciones válidas (sin cardinalidad) que tienen variabilidad
configValidasConVariabilidad = df[(df['Valid'] == True) & (df['ContainVariability'] == True) & (df['ContainCardinality'] == False)].shape[0]

# Contar las configuraciones no válidas (sin erroes)
configNoValidas = df[(df['Valid'] == False) & (df['ObjectType'] != 'none')].shape[0]
configNoValidasROWS = df[(df['Valid'] == False) & (df['ObjectType'] != 'none')]

# Contar las configuraciones no validas (sin errores) con variabilidad 
configsNoValidasConVariabilidad = df[(df['Valid'] == False) & (df['ObjectType'] != 'none') & (df['ContainVariability'] == True)].shape[0]

# Contar las configuraciones con errores
configsErroneas = df[(df['ObjectType'] == 'none')].shape[0]

# Imprimir los resultados
print(f"Total valid configurations: {configValidas}")
print(f"Total valid configurations (without variability) with cardinality: {configsValidasConCardinalidad}")
print(f"Total valid configurations (without cardinality) with variability: {configValidasConVariabilidad}")
print(f"Total invalid configurations (without errors): {configNoValidas}")
print(f"Total invalid configurations (without errors) with variability: {configsNoValidasConVariabilidad}")
print(f"Total configurations with errors: {configsErroneas}")

# Calcular el total de configuraciones
print(f"Total configurations read: {df.shape[0]}")

# Agrupar por el número de 'numFeatures' y contar (no contar aquellas configuraciones con variabilidad o errores)
conteos_num_features = df[((df['ObjectType'] != 'none'))]['numFeatures'].value_counts().sort_index()


# Crear un array o diccionario para almacenar la distribucion de configuraciones segun el numero de numFeatures
resultados_num_features = {num: conteos_num_features.get(num, 0) for num in range(0, 735)} # 735 es el numero de caracteristicas del modelo

# Guardar los resultados por número de numFeatures
with open('distConfigs.csv', mode='w', newline='', encoding='utf-8') as csv_file:
  csv_writer = csv.writer(csv_file)
  csv_writer.writerow(['numFeatures', 'numConfigurations'])
  for num_features, count in resultados_num_features.items():
    csv_writer.writerow([num_features, count])

with open ('NonValidConfigs.csv', mode='w', encoding="utf-8") as csv_file:
  csv_writer = csv.writer(csv_file)
  csv_writer.writerow(configNoValidasROWS.columns)
  for index, row in configNoValidasROWS.iterrows():
    if row['ObjectType'] == "CustomResourceDefinition":
      continue
    else:
      csv_writer.writerow(row)