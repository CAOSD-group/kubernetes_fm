# This script downloads repositories from GitHub and extracts YAML files from the repositories. It then filters out the YAML files 
# that are not Kubernetes manifests and saves the information in a CSV file. The CSV file contains the following columns:
# - nombreRepo: Name of the repository
# - numRepoIntervalo: Number of the repository in the search interval
# - YAMLsEncontrados: Number of YAML files found in the repository
# - stringBusqueda: Search string used on GitHub
# - pagBusqueda: Search page on GitHub
# - url: URL of the search on GitHub
# Finally, it displays on the screen the number of analyzed repositories, the number of YAML files found, and the number of 
# YAML files that are not Kubernetes manifests.
# To download the repositories, the GitHub API is used. An authentication token must be provided in the "github_token" 
# environment variable. The token must have permissions to read public repositories. To obtain a GitHub token, follow the 
# instructions at https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token.

import requests
import git
import os
import shutil
import psutil
import stat
import search_YAMLs
import filter_Manifest
import csv
import time

# Year 2024 divided into periods of 10-11 days
year2024 = [
    "created:2024-01-01..2024-01-10",
    "created:2024-01-11..2024-01-20",
    "created:2024-01-21..2024-01-31",
    "created:2024-02-01..2024-02-10",
    "created:2024-02-11..2024-02-20",
    "created:2024-02-21..2024-02-29",
    "created:2024-03-01..2024-03-10",
    "created:2024-03-11..2024-03-20",
    "created:2024-03-21..2024-03-31",
    "created:2024-04-01..2024-04-10",
    "created:2024-04-11..2024-04-20",
    "created:2024-04-21..2024-04-30",
    "created:2024-05-01..2024-05-10",
    "created:2024-05-11..2024-05-20",
    "created:2024-05-21..2024-05-31",
    "created:2024-06-01..2024-06-10",
    "created:2024-06-11..2024-06-20",
    "created:2024-06-21..2024-06-30",
    "created:2024-07-01..2024-07-10",
    "created:2024-07-11..2024-07-20",
    "created:2024-07-21..2024-07-31",
    "created:2024-08-01..2024-08-10",
    "created:2024-08-11..2024-08-20",
    "created:2024-08-21..2024-08-31",
    "created:2024-09-01..2024-09-10",
    "created:2024-09-11..2024-09-20",
    "created:2024-09-21..2024-09-30",
    "created:2024-10-01..2024-10-10",
    "created:2024-10-11..2024-10-20",
    "created:2024-10-21..2024-10-31",
    "created:2024-11-01..2024-11-10",
    "created:2024-11-11..2024-11-20",
    "created:2024-11-21..2024-11-30",
    "created:2024-12-01..2024-12-10",
    "created:2024-12-11..2024-12-20",
    "created:2024-12-21..2024-12-31"
]

# GitHub configuration
github_token = os.getenv("github_token") # My GitHub token
github_user = 'GITHUB_USER'

# Remaining variables
query = 'Kubernetes' # String to search on GitHub
clonar_en_directorio = 'Repositories/' # Directory where downloaded repositories are stored
destYAML = "YAMLs" # Directory where .yaml files are stored
destNonYAML = "NonYAMLs" # Directory where .yaml files that are not Kubernetes manifests are stored
numAllRepos = 0 # Total number of downloaded repositories
numAllYamls = 0 # Total number of .yaml files found
numAllNonYamls = 0 # Total number of .yaml files that were not Kubernetes manifests
fieldnames = ["nombreRepo", "numRepoIntervalo", "YAMLsEncontrados", "stringBusqueda", "pagBusqueda", "url"] # Column names of the CSV

# Remove a hidden directory
def remove_readonly(func, path, _):
    archivo_en_uso(ruta_repositorio)
    # Elimina los permisos de "read-only"
    os.chmod(path, stat.S_IWRITE)
    func(path)

# Function to search repositories on GitHub
def buscar_repositorios(query, github_user, github_token, page, month):
    time.sleep(2)
    url = f'https://api.github.com/search/repositories?q={query}+{month}&page={page}&per_page=100&sort=stars&order=desc'
    print(f"Downloading repositories from the URL -> {url}")
    response = requests.get(url, auth=(github_user, github_token))
    if response.status_code == 200:
        return response.json()['items'], response.json()['total_count'], url
    else:
        response.raise_for_status()

# Check if a file or directory is in use by another process (necessary to delete it)
def archivo_en_uso(ruta):
    ruta_real = os.path.realpath(ruta)
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for item in proc.open_files():
                if item.path == ruta_real:
                    return True, proc.info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False, None

# Delete the repository folder that is no longer needed
def eliminar_repo(ruta_repositorio):
    archivo_en_uso(ruta_repositorio)
    try:
        shutil.rmtree(ruta_repositorio, onerror=remove_readonly)
        print(f"The repository has been successfully deleted.")
    except Exception as e:
        print(f"Error deleting the repository{ruta_repositorio}: {e}")

# Function to clone a repository
def clonar_repositorio(repo, directorio_destino):
    print(f"Cloning {repo['clone_url']}...")
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
    try:
        repo = git.Repo.clone_from(repo['clone_url'], directorio_destino)
        print(f"Repository {directorio_destino} cloned successfully.")
    except:
        print('There was a problem with the cloning.')
    # Remove "read-only" permissions
    quitar_solo_lectura(directorio_destino)
    return repo

# Function to remove read permissions from a directory
def quitar_solo_lectura(directorio):
    print(f'Removing read-only permissions...')
    for root, dirs, files in os.walk(directorio):
        for nombre in files:
            ruta_archivo = os.path.join(root, nombre)
            # Remove the read-only attribute from the file
            os.chmod(ruta_archivo, stat.S_IWRITE)

        for nombre in dirs:
            ruta_directorio = os.path.join(root, nombre)
            # Remove the read-only attribute from the directory
            os.chmod(ruta_directorio, stat.S_IWRITE)

with open(query+'.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header (column names)
    writer.writeheader()

    for interval in year2024:
        page = 1
        # First search to find how many repositories are found
        repositoriosURL, numMaxRepo, urlGitHub = buscar_repositorios(query, github_user, github_token, 1, interval)
        numRepo = 1 # Repository from which the execution is running
        maxPage = (numMaxRepo//100) +1 # Total pages in the performed search
        numAllRepos += numMaxRepo

        while numRepo <= numMaxRepo and numRepo <= 1000 and page <= maxPage:
            for repoURL in repositoriosURL:
                print(f"<---- Repository {numRepo} of {numMaxRepo} ---->")
                ruta_repositorio = clonar_en_directorio+repoURL['full_name']
                repo = clonar_repositorio(repoURL, ruta_repositorio)

                # Save all the YAML files from that repository
                numYamls = search_YAMLs.main(ruta_repositorio, destYAML)
                numAllYamls += numYamls
                # Delete the repository
                eliminar_repo(clonar_en_directorio)
                # Store the information in the CSV
                data = {"nombreRepo": repoURL['full_name'], "numRepoIntervalo": numRepo, "YAMLsEncontrados": numYamls, "stringBusqueda": query, "pagBusqueda": page, "url": urlGitHub}
                writer.writerow(data)
                numRepo += 1
            page +=1
            if page <= maxPage and numRepo <= 1000 and numRepo <= numMaxRepo: 
                repositoriosURL, numMaxRepo, urlGitHub = buscar_repositorios(query, github_user, github_token, page, interval)
            
    # Filter those .yaml files that are not Kubernetes manifests
    numAllNonYamls = filter_Manifest.main(destYAML, destNonYAML)

    print(f'\nA total of {numAllRepos} repositories have been analyzed, finding {numAllYamls} .yaml files, of which {numAllNonYamls} have been discarded.')