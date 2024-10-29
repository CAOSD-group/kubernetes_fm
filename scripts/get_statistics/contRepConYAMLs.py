# This script counts the repositories with Kubernetes manifests, and calculates the standard deviation, median, 
# and mode of the values greater than zero in the "YAMLsFound" column of CSV files. The results are displayed in the terminal.

import pandas as pd
import numpy as np
from statistics import mode, StatisticsError

# Lista de archivos CSV
archivos_csv = ['scripts/resources/Kubernetes_validator_search/Kubernetes_validator.csv', 
                'scripts/resources/Kubernetes_manifest_search/Kubernetes_manifest.csv', 
                'scripts/resources/Kubernetes_search/Kubernetes.csv']

# Inicializar el contador y el array
total_filas_con_valor_mayor_cero = 0
total_archivos = 0
total_filas = 0
valores_mayores_cero = []

# Recorrer cada archivo CSV
for archivo in archivos_csv:
    # Leer el CSV
    df = pd.read_csv(archivo)
    
    # Filtrar las filas donde "YAMLsEncontrados" es mayor que cero
    filas_mayor_cero = df[df['YAMLsEncontrados'] > 0]
    total_filas += df.shape[0]

    # Contar los archivos YAML encontrados
    total_archivos += df['YAMLsEncontrados'].sum()

    # Ver el maximo de YAMLs encontrados en un repositorio
    max = df['YAMLsEncontrados'].max()

    # Ver el minimo de YAMLs encontrados en un repositorio
    min = df['YAMLsEncontrados'].min()
    
    # Contar las filas
    total_filas_con_valor_mayor_cero += filas_mayor_cero.shape[0]
    
    # Almacenar los valores mayores que cero en el array
    valores_mayores_cero.extend(filas_mayor_cero['YAMLsEncontrados'].tolist())

# Imprimir el total de filas
print(f'Total Repositories: {total_filas}')

# Imprimir el total de filas con valores mayores que cero
print(f'Total Repositories with at least one Kubernetes manifest: {total_filas_con_valor_mayor_cero}')

# Imprimir el maximo de YAMLs encontrados en un repositorio
print(f'Maximum YAMLs found in a repository: {max}')

# Imprimir el minimo de YAMLs encontrados en un repositorio
print(f'Minimum YAMLs found in a repository: {min}')

# Imprimir el total de filas
print(f'Total YAML files found (not necessarily manifests): {total_archivos}')

# Imprimir el array con los valores mayores que cero
# print(f'Valores mayores que cero: {valores_mayores_cero}')

# Calcular las estadísticas si hay valores mayores que cero
if valores_mayores_cero:
    # Desviación típica
    desviacion_tipica = np.std(valores_mayores_cero, ddof=0)  # ddof=1 para la muestra
    print(f'Standard deviation: {desviacion_tipica}')
    
    # Mediana
    mediana = np.median(valores_mayores_cero)
    print(f'Median: {mediana}')
    
    # Moda usando statistics.mode
    try:
        moda = mode(valores_mayores_cero)
        print(f'Mode: {moda}')
    except StatisticsError:
        print('There is no single mode value.')
else:
    print('There are no values greater than zero to calculate the statistics.')
