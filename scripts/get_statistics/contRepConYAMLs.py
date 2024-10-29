# Este script cuenta los repositorios con manifiestos de kubernetes, y calcula la desviación típica, mediana y moda de los valores 
# mayores que cero de la columna "YAMLsEncontrados" de los archivos CSV. Los resultados se muestran por la terminal.

import pandas as pd
import numpy as np
from statistics import mode, StatisticsError

# Lista de archivos CSV
archivos_csv = ['scripts/resources/Busqueda_KubernetesKubernetes_validator.csv', 
                'scripts/resources/Busqueda_KubernetesKubernetes_manifest.csv', 
                'scripts/resources/Busqueda_Kubernetes/Kubernetes.csv']

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
print(f'Total de Repositorios: {total_filas}')

# Imprimir el total de filas con valores mayores que cero
print(f'Total de Repositorios con algun manifiesto de kubernetes: {total_filas_con_valor_mayor_cero}')

# Imprimir el maximo de YAMLs encontrados en un repositorio
print(f'Maximo de YAMLs encontrados en un repositorio: {max}')

# Imprimir el minimo de YAMLs encontrados en un repositorio
print(f'Minimo de YAMLs encontrados en un repositorio: {min}')

# Imprimir el total de filas
print(f'Total de archivos YAML encontrados (No necesariamente manifiestos): {total_archivos}')

# Imprimir el array con los valores mayores que cero
# print(f'Valores mayores que cero: {valores_mayores_cero}')

# Calcular las estadísticas si hay valores mayores que cero
if valores_mayores_cero:
    # Desviación típica
    desviacion_tipica = np.std(valores_mayores_cero, ddof=0)  # ddof=1 para la muestra
    print(f'Desviación típica: {desviacion_tipica}')
    
    # Mediana
    mediana = np.median(valores_mayores_cero)
    print(f'Mediana: {mediana}')
    
    # Moda usando statistics.mode
    try:
        moda = mode(valores_mayores_cero)
        print(f'Moda: {moda}')
    except StatisticsError:
        print('No hay un único valor que sea moda.')
else:
    print('No hay valores mayores que cero para calcular las estadísticas.')
