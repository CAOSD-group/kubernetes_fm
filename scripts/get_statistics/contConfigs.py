# This script reads configuration data from a CSV file and computes some basic statistical measures 
# (total, standard deviation, median, and mode) on that data.

import pandas as pd
import numpy as np
from statistics import mode, StatisticsError

# Read the CSV file.
df = pd.read_csv('numConfPerManifest.csv')

# Create an array with the entries from the 'numConfigurations' column
array_num_configurations = df['numConfigurations'].tolist()
numConfigs = df['numConfigurations'].sum()

# Total configurations
print(f'Total configurations {numConfigs}')

# Standard deviation
desviacion_tipica = np.std(array_num_configurations, ddof=0) 
print(f'Standard deviation: {desviacion_tipica}')

# Median
mediana = np.median(array_num_configurations)
print(f'Median: {mediana}')

# Mode using statistics.mode
try:
    moda = mode(array_num_configurations)
    print(f'Mode: {moda}')
except StatisticsError:
    print('There is no single mode value.')

# Maximum and minimum
valor_maximo = df['numConfigurations'].max()
valor_minimo = suma_numConfigs = df[df['numConfigurations'] > 0]['numConfigurations'].min()

print(f'Maximum configurations in a manifest: {valor_maximo}')
print(f'Minimun configurations in a manifest: {valor_minimo}')