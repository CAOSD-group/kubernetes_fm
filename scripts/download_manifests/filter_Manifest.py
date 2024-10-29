# This script iterates through all the files in a folder and checks if it is a Kubernetes YAML by verifying 
# if the words apiVersion and kind exist.

import os
import shutil

def is_kubernetes_manifest(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contenido = file.read()
            return 'apiVersion' in contenido and 'kind' in contenido
    except UnicodeDecodeError:
        return False
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return False

# Recorre todos los archivos en la carpeta
def main(folder_path, destnonyamls):
    print(f"Removing files that are not Kubernetes manifests...")
    eliminated = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            if not is_kubernetes_manifest(file_path):
                if not os.path.exists(destnonyamls):
                     os.makedirs(destnonyamls)
                shutil.copy2(file_path, destnonyamls)
                os.remove(file_path)
                eliminated += 1
    print(f"{eliminated} files have been deleted.")    
    return eliminated