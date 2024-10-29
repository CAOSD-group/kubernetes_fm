# This script reads configuration data from a CSV file and computes some basic statistical measures 
# (total, standard deviation, median, and mode) on that data.

import pandas as pd
import numpy as np
from statistics import mode, StatisticsError

# Leer el archivo CSV
df = pd.read_csv('numConfPerManifest.csv')

# Crear un array con las entradas de la columna 'numConfigurations'
array_num_configurations = df['numConfigurations'].tolist()
numConfigs = df['numConfigurations'].sum()

# Total de configuraciones
print(f'Total configurations {numConfigs}')

#desviación típica
desviacion_tipica = np.std(array_num_configurations, ddof=0) 
print(f'Standard deviation: {desviacion_tipica}')

# Mediana
mediana = np.median(array_num_configurations)
print(f'Median: {mediana}')

# Moda usando statistics.mode
try:
    moda = mode(array_num_configurations)
    print(f'Mode: {moda}')
except StatisticsError:
    print('There is no single mode value.')

# Maximo y minimo
valor_maximo = df['numConfigurations'].max()
valor_minimo = suma_numConfigs = df[df['numConfigurations'] > 0]['numConfigurations'].min()

print(f'Maximum configurations in a manifest: {valor_maximo}')
print(f'Minimun configurations in a manifest: {valor_minimo}')