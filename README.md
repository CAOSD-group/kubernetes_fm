# The Kubernetes variability model
This repository contains the feature model of Kubernetes (K8s) in the [UVL](https://universal-variability-language.github.io/) format.

The repository also contains all the resources associated with the submission of VaMoS'25 entitled: ``The Kubernetes variability model''.

## Artifact description
The repository contains the following resources:
- The [Kubernetes feature model](variability_model/)
- [Real-world configurations](configurations/) of Kubernetes.
- [Scripts](scripts/) to gather the configurations from the GitHub repositories, and to generate configurations from the feature model.
- [Templates](templates/) to generate configurations using the feature model.
- [Mapping](mapping/) with information to map every feature in the model to the generation templates.
- [Configuration examples](generation_example/) in JSON of the K8s feature model to generate final K8s products.


## Usage
The feature model can be directly download from [here](variability_model/KubernetesFM.uvl).

The model can be easily inspected with a text editor or with any application supporting the UVL language. 
Tool support for UVL can be consulted in the [UVL official website](https://universal-variability-language.github.io/).
We recommend the following tools because they fully support the Kubernetes feature model:
- [Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=caradhras.uvls-code) based on [UVLS](https://github.com/Universal-Variability-Language/uvl-lsp) to inspect and edit the feature model, and create new configurations (in JSON) from the feature model.
- [Flamapy](https://flamapy.github.io/) to work with and analyze the feature model.

Since not all tools still support all UVL extensions used in the Kubernetes feature model, we provide a simplified version that can be used with those tools such as a [FeatureIDE](https://featureide.github.io/).

## Extracting, validating, and generating configurations

### Requirements
- [Python 3.9+](https://www.python.org/)
- [Flamapy](https://www.flamapy.org/)
- [UVLS](https://github.com/Universal-Variability-Language/uvl-lsp)

### Download and install
1. Install [Python 3.9+](https://www.python.org/)
2. Clone this repository and enter into the main directory:

    `git clone https://github.com/CAOSD-group/kubernetes_fm.git`

    `cd kubernetes_fm` 
    
3. Create a virtual environment: 
   
   `python -m venv env`

4. Activate the environment: 
   
   In Linux: `source env/bin/activate`

   In Windows: `.\env\Scripts\Activate`

5. Install the dependencies: 
   
   `pip install -r requirements.txt`
   

### Extracting real configurations of Kubernetes from GitHub repositories
First, we need to set up the following variables in the [`download_repositories.py`](scripts/download_manifests/download_repositories.py) script:

```
github_token = os.getenv("github_token")
github_user = 'GITHUB_USER'
```

To generate a user token, go to GitHub, and in your account go to Settings -> Developer Settings -> Personal access tokens -> Tokens (classic) -> Generate new token -> Generate new token (classic).
Create a new .env file in the main folder and declare a new variable:
```
github_token = "copy here your GitHub user token"
```
Additionally, you can set up the string query for search changing the following line:

```
query = 'Kubernetes'
```

Finally, execute:

   `python scripts/download_manifest/download_repositories.py`

This generates:
(1) a new folder "YAMLs" with all K8s manifest files found,
(2) a new folder "NonYAMLs" with all YAML files that are not K8s manifest files, and
(3) a new .csv file with information stats about the process (e.g., repositories visited, number of files, etc.).


### Validating real configurations against the feature model
To validate the extracted configurations against the feature model, execute:

   `python scripts/get_features_from_manifests/extract_features_from_YAML.py`

This generates:
(1) a "Configurations.csv" file with information about the configurations (e.g., features, satisfiability, etc.), and 
(2) a "filesNotProcessed" with those K8s manifest files that couldn't be processed due to syntax error or other reasons (e.g., contain variability).

### Generating configurations from the feature model
To generate new configurations using the feature model, execute:

   `python scripts/main_resolve_variability.py -c <config.json> -m mapping/KubernetesFM_mapping.csv -t templates/KubernetesFM_base.txt.jinja`

   where:
   - `<config.json>` is a JSON file with the configuration of the feature model generated using the  [UVLS](https://github.com/Universal-Variability-Language/uvl-lsp) tool. Three examples of configurations of the K8s feature model are available in the [`generation_example`](generation_example/) folder. You can use one of these examples as follows:
      
      `python scripts/main_resolve_variability.py -c generation_example/KubernetesFM_deployment_example.uvl.json -m mapping/KubernetesFM_mapping.csv -t templates/KubernetesFM_base.txt.jinja`

   - `mapping/KubernetesFM_mapping.csv` is a mapping file stablishing the relationships between the features in the K8s feature model and the parameters in the Jinja templates.
   - `templates/KubernetesFM_base.txt.jinja` is the base parameterized template in Jinja for Kurbenetes.

   This generates a `KubernetesManifest.yaml` file which is the final generated K8s configuration ready to be deployed. 


### Simplify the K8s feature model for interoperability with UVL tools
Since not all tools still support all UVL extensions used in the K8s feature model, we provide a simplified version that can be used with those tools such as a [FeatureIDE](https://featureide.github.io/).
The simplified version of the K8s feature model is available [here](variability_model/KubernetesFM_simple.uvl), and can be generate from the full version executing the following script:
   
   `python scripts/generate_simple_FM.py`


### Other resources
Other resources and utils are available in [`scripts/resources/`](scripts/resources/) such as scripts to generate the "Product Distribution" and "Feature Inclusion Probabilities" .csv files from the extracted configurations as presented in the paper.

