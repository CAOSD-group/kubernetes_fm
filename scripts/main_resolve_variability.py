import sys
import subprocess

import click

from spl_implementation.models import VEngine


# CLICK ARGUMENTS
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

    with open("KubernetesManifest.yaml", "w") as f: # Save the result in a file
        print('\n')
        print_without_blank_lines(result, f)
        print('\n')
    
    if(kubernetes): # Check if exist any error in the kubernetes YAML
        rdo = subprocess.run([kubeconform, "KubernetesManifest.yaml"], capture_output=True, text=True)
        if (rdo.stdout != ''):
            print(f"\033[91m ERROR: {rdo.stdout} \033[0m") # Print the result of the check in red
        if(details):
            details = subprocess.run([kube_score, "score", "KubernetesManifest.yaml"], capture_output=True, text=True) # Analiza el resultado en busca de recomendaciones
            print(f"\033[92m RECOMMENDATIONS: {details.stdout} \033[0m")
    if (dockerfile):
         rdo = subprocess.run([hadolint, "KubernetesManifest.yaml"], capture_output=True, text=True)
         print(f"\033[91m ERROR: {rdo.stdout} \033[0m") # Print the result of the check in red
def print_without_blank_lines(text, file):
    for line in text.splitlines():
        if line.strip():  # Verify if the line is not blank
            sys.stdout.write(line + '\n')  # Write the line in stdout
            file.write(line + '\n')

if __name__ == '__main__':
    main()