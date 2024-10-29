import pandas as pd
import numpy as np
from statistics import mode, StatisticsError

# Leer el archivo CSV
df = pd.read_csv('numConfPerManifest.csv')

# Crear un array con las entradas de la columna 'numConfigurations'
array_num_configurations = df['numConfigurations'].tolist()
numConfigs = df['numConfigurations'].sum()

# Total de configuraciones
print(f'Total de configuraciones: {numConfigs}')

#desviación típica
desviacion_tipica = np.std(array_num_configurations, ddof=0) 
print(f'Desviación típica: {desviacion_tipica}')

# Mediana
mediana = np.median(array_num_configurations)
print(f'Mediana: {mediana}')

# Moda usando statistics.mode
try:
    moda = mode(array_num_configurations)
    print(f'Moda: {moda}')
except StatisticsError:
    print('No hay un único valor que sea moda.')

# Maximo y minimo
valor_maximo = df['numConfigurations'].max()
valor_minimo = suma_numConfigs = df[df['numConfigurations'] > 0]['numConfigurations'].min()

print(f'Maximo de configuraciones en un manifiesto: {valor_maximo}')
print(f'Minimo de configuraciones en un manifiesto: {valor_minimo}')