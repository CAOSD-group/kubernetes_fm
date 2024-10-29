import os
import argparse
import csv
import sys
from typing import Any

import jinja2

from spl_implementation.utils import utils
from spl_implementation.models import VEngine
import subprocess

import click

# ARGUMENTOS CLICK
@click.command()
@click.option('--config', '-c', required=True, type=click.Path(exists=True), default='', help='Configuration file path of the FM')
@click.option('--map', '-m', required=True, type=click.Path(exists=True), default='', help='Mapping file path')
@click.option('--template', '-t', required=True, type=click.Path(exists=True), default='', help='Template file path')
@click.option('--kubernetes', '-k', is_flag=True, help='Indicate if the result validity should be checked for Kubernetes')
@click.option('--details', is_flag=True, help='Indicate if YAML file optimization details should be provided')
@click.option('--dockerfile', '-d', is_flag=True, help='Indicate if the result should be validated for Kubernetes')

def main(config, map, template, kubernetes, details, dockerfile):
    kubeconform = "scripts/validators/kubeconform.exe"
    kube_score = "scripts/validators/kube-score.exe"
    hadolint = 'scripts/validators/hadolint.exe'
    vengine = VEngine()

    vengine.load_configuration(config)
    vengine.load_mapping_model(map)
    vengine.load_template(template)

    result = vengine.resolve_variability()

    with open("KubernetesManifest.yaml", "w") as f: # Guarda el resultado en un fichero 
        print('\n')
        print_without_blank_lines(result, f)
        print('\n')
    
    if(kubernetes): # Comprueba si existe algun error en el YAML de kubernetes
        rdo = subprocess.run([kubeconform, "KubernetesManifest.yaml"], capture_output=True, text=True)
        if (rdo.stdout != ''):
            print(f"\033[91m ERROR: {rdo.stdout} \033[0m") # Imprime el resultado de la comprobacion en rojo
        if(details):
            details = subprocess.run([kube_score, "score", "KubernetesManifest.yaml"], capture_output=True, text=True) # Analiza el resultado en busca de recomendaciones
            print(f"\033[92m RECOMMENDATIONS: {details.stdout} \033[0m")
    if (dockerfile):
         rdo = subprocess.run([hadolint, "KubernetesManifest.yaml"], capture_output=True, text=True)
         print(f"\033[91m ERROR: {rdo.stdout} \033[0m") # Imprime el resultado de la comprobacion en rojo
def print_without_blank_lines(text, file):
    for line in text.splitlines():
        if line.strip():  # Verifica si la línea no está en blanco
            sys.stdout.write(line + '\n')  # Escribe la línea en stdout
            file.write(line + '\n')

if __name__ == '__main__':
    main()