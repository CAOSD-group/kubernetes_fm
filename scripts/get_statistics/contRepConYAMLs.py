# This script counts the repositories with Kubernetes manifests, and calculates the standard deviation, median, 
# and mode of the values greater than zero in the "YAMLsFound" column of CSV files. The results are displayed in the terminal.

import pandas as pd
import numpy as np
from statistics import mode, StatisticsError

# List of CSV files
archivos_csv = ['scripts/resources/Kubernetes_validator_search/Kubernetes_validator.csv', 
                'scripts/resources/Kubernetes_manifest_search/Kubernetes_manifest.csv', 
                'scripts/resources/Kubernetes_search/Kubernetes.csv']

# Initialize the counter and the array
total_filas_con_valor_mayor_cero = 0
total_archivos = 0
total_filas = 0
valores_mayores_cero = []

# Traverse each CSV file
for archivo in archivos_csv:
    # Read the CSV file
    df = pd.read_csv(archivo)
    
    # Filter the rows where "YAMLsEncontrados" is greater than zero
    filas_mayor_cero = df[df['YAMLsEncontrados'] > 0]
    total_filas += df.shape[0]

    # Count the YAML files found.
    total_archivos += df['YAMLsEncontrados'].sum()

    # See the maximum number of YAMLs found in a repository
    max = df['YAMLsEncontrados'].max()

    # See the minimum number of YAMLs found in a repository
    min = df['YAMLsEncontrados'].min()
    
    # Count the rows.
    total_filas_con_valor_mayor_cero += filas_mayor_cero.shape[0]
    
    # Store the values greater than zero in the array
    valores_mayores_cero.extend(filas_mayor_cero['YAMLsEncontrados'].tolist())

# Print the total number of repositories
print(f'Total Repositories: {total_archivos}')

# Print the total number of rows with values greater than zero
print(f'Total Repositories with at least one Kubernetes manifest: {total_filas_con_valor_mayor_cero}')

# Print the maximum number of YAMLs found in a repository
print(f'Maximum YAMLs found in a repository: {max}')

# Print the minimum number of YAMLs found in a repository
print(f'Minimum YAMLs found in a repository: {min}')

# Print the total number of rows
print(f'Total YAML files found (not necessarily manifests): {total_filas}')

# Print the array with values greater than zero
# print(f'Valores mayores que cero: {valores_mayores_cero}')

# Calculate the statistics if there are values greater than zero
if valores_mayores_cero:
    # Standard deviation
    desviacion_tipica = np.std(valores_mayores_cero, ddof=0)  # ddof=1 para la muestra
    print(f'Standard deviation: {desviacion_tipica}')
    
    # Median
    mediana = np.median(valores_mayores_cero)
    print(f'Median: {mediana}')
    
    # Mode using statistics.mode
    try:
        moda = mode(valores_mayores_cero)
        print(f'Mode: {moda}')
    except StatisticsError:
        print('There is no single mode value.')
else:
    print('There are no values greater than zero to calculate the statistics.')
