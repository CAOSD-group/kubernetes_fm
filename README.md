# The Kubernetes variability model
This repository contains the feature model of Kubernetes in the [UVL](https://universal-variability-language.github.io/) format.

The repository also contains all the resources associated with the submission of VaMoS'25 entitled: ``The Kubernetes variability model''.

## Artifact description
The repository contains the following resources:
- The [Kubernetes feature model](variability_model/)
- [Real-world configurations](configurations/) of Kubernetes.
- [Scripts](scripts/) to gather the configurations from the GitHub repositories, and to generate configurations from the feature model.
- [Templates](templates/) to generate configurations using the feature model.
- [Mapping](mapping/) with information to map every feature in the model to the generation templates.

## Usage
The feature model can be directly download from [here](variability_model/KubernetesFM.uvl).

The model can be easily inspected with a text editor or with any application supporting the UVL language. 
Tool support for UVL can be consulted in the [UVL official website](https://universal-variability-language.github.io/).
We recommend the following tools because they fully support the Kubernetes feature model:
- [Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=caradhras.uvls-code) based on [UVLS](https://github.com/Universal-Variability-Language/uvl-lsp) to inspect and edit the feature model.
- [Flamapy](https://flamapy.github.io/) to work with and analyze the feature model.

Since not all tools still support all UVL extensions used in the Kubernetes feature model, we provide a simplified version that can be used with those tools such as a [FeatureIDE](https://featureide.github.io/).

## Extracting, validating, and generating configurations

### Requirements
- [Python 3.9+](https://www.python.org/)
- [Flamapy](https://www.flamapy.org/)

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
   


### Extracting real-world configurations of Kubernetes from GitHub repositories
To extract the real-world configurations from GitHub repositories, execute:

   `python run.py`

Configurations will stored in...

### Validating real-world configurations against the feature model
To validate the extracted configurations against the feature model, execute:

   `python run.py`


### Generating configurations from the feature model
To generate new configurations using the feature model, follow these steps:
1.
2.

### Other resources
