# This script extracts the keys from the YAML files and saves them in a CSV file. The CSV file contains the following columns:
#   File: Name of the YAML file
#   ObjectType: Type of YAML object (only if it is a Kubernetes manifest)
#   Valid: Indicates whether the YAML file is valid or not
#   numFeatures: Number of features in the YAML file
#   ContainVariability: Indicates whether the YAML file contains variability or not
#   Error: Indicates if there was an error when verifying whether it was a valid configuration
#   Config: Keys of the YAML file
#   featuresNotFound: Keys found in the YAML file that are not in the feature model
# It also generates a CSV file with the number of configurations per manifest (including those where no configurations were found) and a file with the unprocessed files.

import re
import yaml
import csv
from tqdm import tqdm
import os
import valid_config
import socket

output_csv = "Configurations.csv" # Output CSV file path
output_numConfPerManifest_csv = "numConfPerManifest.csv" # Path of the CSV file with the number of configurations per manifest
output_not_processed = "filesNotProcessed.txt" # Path of the file with the unprocessed files
folder_path = "YAMLs" # Path of the folder with the YAML files
mapping_file = "scripts/resources/mapping_features_keys.csv" # Path of the mapping file
model_path = "variability_model/KubernetesFM_simple.uvl" # Path of the feature model
fm_model, sat_model = valid_config.inizialize_model(model_path) # Initialize the models (More efficient to load them only once)
values_of_keys = [] # List to store the key values
variability = False # Indicate if the configuration contains variability
cardinality = False # Indicate if the configuration contains cardinality

# Validate if a value is an IP address (IPv4 or IPv6)
def is_ip(value):
    try:
        # Try to validate as IPv4
        socket.inet_pton(socket.AF_INET, value)
        return True
    except socket.error:
        pass  # It is not a valid IPv4
    try:
        # Try to validate as IPv6
        socket.inet_pton(socket.AF_INET6, value)
        return True
    except socket.error:
        pass  # It is not a valid IPv6
    return False

# Recursive function to extract all the keys, including nested ones, from a Kubernetes object declaration
def extract_keys(data, parent_key='', kind=None):
    global values_of_keys
    keys = []
    values = []
    global cardinality
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{parent_key}_{key}" if parent_key else key
            # If the key starts with 'spec', the value of 'kind' is added as a prefix, generating "deploymentspec" or "servicespec" for example
            if key == 'spec' and parent_key == '':
                full_key = f"{kind}{key}"
            if parent_key.startswith('spec'): 
                full_key = f"{kind}{parent_key}_{key}"
            if isinstance(value, str):
                if is_ip(value): # If the value is an IP, it is added as "key_IP_value"
                    full_value = f"{full_key}_IP"
                else:
                    full_value = f"{full_key}_{value}"
                values_of_keys.append(full_value)
            keys.append(full_key)    
            keys.extend(extract_keys(value, full_key, kind))
    # If it is a list, each element of the list is processed
    elif isinstance(data, list): 
        full_key = f"{parent_key}"
        cardinality = True
        for index, item in enumerate(data):
            if isinstance(item, str) and is_ip(item):
                values_of_keys.append(full_key + "_IP") 
            else:
                keys.extend(extract_keys(item, full_key, kind))      
    return list(set(keys)) # Remove duplicates

# Function to translate the keys of the YAML files into feature model characteristics.
def translate_keys(keys, map1, map2):
    # List to store the mapped keys
    mapped_keys = []
    keys_not_found = []

    
    # Process each key
    for key in keys:
  
        if key in map2:
            # If it is in the 3rd column, replace it with the value of the 1st column
            mapped_keys.append(map2[key])
        elif key in map1:
            # If it is in the 2nd column, replace it with the value of the 1st column
            mapped_keys.append(map1[key])
        else:
            # If it is not found in any column, leave the key as is
           keys_not_found.append(key)
    return mapped_keys, keys_not_found

# Obtain the group and version of the Kubernetes object
def get_group_and_version(doc):
    var = doc.get('apiVersion', '').split('/')
    kind = doc.get('kind', '')
    if len(var) == 2:
        group, version = var
    else:
        group = 'core'
        version = var[0]
    return group, version, kind

# Check if the manifest contains variability
def check_variability(yaml_data):
    # Convert the YAML to a string to search for variability in each line
    yaml_str = yaml.dump(yaml_data)
    # We use a regular expression to find "{{ something }}" in the YAML
    variable_pattern = re.compile(r'\{\{.*?\}\}')
    # If we find matches, return True; if not, return False.
    return bool(variable_pattern.search(yaml_str))

# Extract all the features of the objects defined in the YAML file (more than one object can be defined in a YAML file).
def read_keys_yaml(file_path, map1, map2):
    keys = []
    kinds = []
    not_found = []
    cardinalities = []
    variabilities = []
    configs = 0
    global values_of_keys
    global cardinality
    global variability
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        # Load all the YAML documents (including the '---' separators)
        documents = yaml.safe_load_all(file)
        for doc in documents:
            if doc is None:
                continue
            values_of_keys = []
            cardinality = False
            variability = False
            configs += 1 # Count the number of configurations in the YAML file.
            # Check if the manifest contains variability
            variability = check_variability(doc)
            variabilities.append(variability)
            # Obtain the values of 'group', 'version', and 'kind' (to know how to prefix the keys) in order to include those keys.
            group_value, version_value, kind_value = get_group_and_version(doc)
            # Obtain all the keys from the YAML document
            keys_doc = extract_keys(doc, kind = kind_value.lower()) 
            values_doc, values_not_found = translate_keys(values_of_keys, map1, map2)
            keys_doc.append(kind_value)
            keys_doc.append(group_value)
            keys_doc.append(version_value)
            # Translate the keys.
            keys_doc, keys_not_found = translate_keys(keys_doc, map1, map2) 
            # The features found as the value of a key are added to the list of keys in the manifest.
            for value in values_doc:
                if value not in keys_doc:
                    keys_doc.append(value)
            keys.append(keys_doc)
            kinds.append(kind_value)
            cardinalities.append(cardinality)
            not_found.append(keys_not_found)
    return keys, kinds, not_found, configs, cardinalities, variabilities

# Save the keys in a CSV file.
def save_keys_csv(objectType, keys, filename, variabilities, cardinalities, not_found, csv_writer):
    for key_list, objectType, variability, not_found, cardi in zip(keys, objectType, variabilities, not_found, cardinalities):
        isValid, error, complete_config = valid_config.main(key_list, fm_model, sat_model, cardi) # "complete_config" is the complete configuration according to the model.
        csv_writer.writerow([filename, objectType, isValid, len(complete_config), variability, cardi, error, complete_config, not_found])

# Read the CSV file and build the mapping table.
def create_mapping(mapping_file):
    mapping_table = []
    with open(mapping_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header.
        for row in reader:
            if len(row) >= 3:  # Make sure there are at least 3 columns
                mapping_table.append((row[0], row[1], row[2]))
    # Create dictionaries map1 and map2 
    map1 = {n2: n1 for n1, n2, _ in mapping_table}
    map2 = {n3: n1 for n1, _, n3 in mapping_table}
    return map1, map2

if __name__ == '__main__':
    numFilesNotProcessed = 0
    filesNotProcessed = []
    numConfPerManifest = {}
    # Create the CSV file and write the header
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['File', 'ObjectType', 'Valid', 'numFeatures', 'ContainVariability', 'ContainCardinality', 'Error', 'Config', 'featuresNotFound'])
        
        # Proceess each YAML file in the folder
        for filename in tqdm(os.listdir(folder_path)): # tqdm para mostrar una barra de progreso
            configs = 0
            # Get the full path of the file
            file_path = os.path.join(folder_path, filename)
            # Create dictionaries map1 and map2 to translate the yaml keys to FM features (more efficient)
            map1, map2 = create_mapping(mapping_file) 
            try:
                # Get the features of the YAML file
                values_of_keys = []
                keys, objectType, not_found, configs, cardinalities, variabilities = read_keys_yaml(file_path, map1, map2) 
                # Store the number of configurations per manifest
                numConfPerManifest[filename] = configs
                # Store the features in the CSV file
                save_keys_csv(objectType, keys, filename, variabilities, cardinalities, not_found, csv_writer) 
            # handle exceptions
            except yaml.YAMLError as e:
                # If there is an error extracting the features from the YAML file...
                numFilesNotProcessed += 1
                error_message = str(e)
                filesNotProcessed.append((filename, error_message))
                numConfPerManifest[filename] = configs
                # Make distinction between these errors because they occur when there is variability "{{}}"
                if "while parsing a block mapping" or "while parsing a flow node" in error_message:
                    save_keys_csv(['none'], [''], filename, {True}, [False], [''], csv_writer)
                else:
                    save_keys_csv(['none'], [''], filename, {False}, [False], [''], csv_writer)
                continue
            except Exception as e:
                numFilesNotProcessed += 1
                error_message = str(e)
                filesNotProcessed.append((filename, error_message))
                numConfPerManifest[filename] = configs
                # Make distinction between these errors because they occur when there is variability "{{}}"
                if "while constructing a mapping" or "while scanning a simple key" in error_message:
                    save_keys_csv(['none'], [''], filename, {True}, [False], [''], csv_writer)
                else:
                    save_keys_csv(['none'], [''], filename, {False}, [False], [''], csv_writer)
                continue
    # Store the unprocessed files
    with open(output_not_processed, mode='w', newline='', encoding='utf-8') as file:
        file.write(f'Unable to process {numFilesNotProcessed} files. \n\n')
        for (filename, err) in filesNotProcessed:
            file.write(f'file: {filename} ')
            file.write(f'error: {err}')
            file.write(f'\n <------------------------------------> \n')
    # Store the number of configurations per manifest
    with open(output_numConfPerManifest_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['File', 'numConfigurations'])
        for key, value in numConfPerManifest.items():
            csv_writer.writerow([key, value])

    # Show completion message
    print(f"The keys have been saved in {output_csv}.")
    print(f"Unable to process {numFilesNotProcessed} files. The list can be found in {output_not_processed}.")
