# Obtiene el numero de configuraciones validas, no validas, con variabilidad y con errores de un archivo CSV y guarda la 
# distribucion de configuraciones segun el numero de caracteristicas en un archivo CSV. Tambien guarda un CSV con las 
# configuraciones fallidas.

import csv
import pandas as pd

# Ruta del archivo CSV
ruta_csv = r'C:\Users\CAOSD\Documents\githubScraping\Configuraciones.csv'

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
print(f"Total de configuraciones válidas: {configValidas}")
print(f"Total de configuraciones válidas (sin variabilidad) con cardinalidad: {configsValidasConCardinalidad}")
print(f"Total de configuraciones válidas (sin cardinalidad) con variabilidad: {configValidasConVariabilidad}")
print(f"Total de configuraciones no válidas (sin errores): {configNoValidas}")
print(f"Total de configuraciones no válidas (sin errores) con variabilidad: {configsNoValidasConVariabilidad}")
print(f"Total de configuraciones con error: {configsErroneas}")

# Calcular el total de configuraciones
print(f"Total de configuraciones leidas: {df.shape[0]}")

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

with open ('configsNoValidas.csv', mode='w', encoding="utf-8") as csv_file:
  csv_writer = csv.writer(csv_file)
  csv_writer.writerow(configNoValidasROWS.columns)
  for index, row in configNoValidasROWS.iterrows():
    if row['ObjectType'] == "CustomResourceDefinition":
      continue
    else:
      csv_writer.writerow(row)