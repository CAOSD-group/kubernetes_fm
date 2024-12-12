# Script that counts the most common features in YAML files from a folder and saves the results in a CSV.
# It also adds features from the FM that were not found in the YAML with zero occurrences.
# The columns of the CSV are:
# - feature: Key from the YAML file
# - Count: Number of times the key appears
# - Percentage: Percentage of occurrences of the key in relation to the most common key
# It also saves a CSV file with the number of configurations per manifest (including those where no configurations were found).

import os
import yaml
from collections import Counter
import pandas as pd
from tqdm import tqdm
import csv
from flamapy.metamodels.configuration_metamodel.models import Configuration
from flamapy.metamodels.fm_metamodel.models import FeatureModel, Feature
from flamapy.metamodels.fm_metamodel.transformations import UVLReader
from flamapy.metamodels.pysat_metamodel.models import PySATModel
from flamapy.metamodels.pysat_metamodel.transformations import FmToPysat
from flamapy.metamodels.pysat_metamodel.operations import PySATSatisfiableConfiguration
import socket

mapping_file = 'mapping\KubernetesFM_mapping.csv' 
fm_file = 'variability_model\KubernetesFM_simple.uvl'
folder_path = 'YAMLs'  # Path of the folder with .yaml files
output_csv = 'most_common_features.csv'  # Path where the CSV will be saved
output_numConfPerManifest_csv = 'numConfPerManifest.csv'  # Path where the CSV with the number of configurations per manifest will be saved
map1 = {} # Dictionary key (feature) -> value (string)
map2 = {} # Dictionary key (feature) -> value (string)

# Read the CSV file and build the mapping table
def create_mapping(mapping_file):
    mapping_table = []
    global map1
    global map2
    with open(mapping_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            if len(row) >= 3:  # Ensure that there are at least 3 columns
                mapping_table.append((row[0], row[1], row[2]))
    # Create the dictionaries map1 and map2
    map1 = {n2: n1 for n1, n2, _ in mapping_table}
    map2 = {n3: n1 for n1, _, n3 in mapping_table}

# Validate if a value is an IP (IPv4 or IPv6)
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

# Extract the keys from a YAML file
def extract_keys(yaml_content, kind,  parent_key=''):
    keys = []
    if isinstance(yaml_content, dict):
        for key, value in yaml_content.items():
            if isinstance(key, str):  # Ensure that the key is a string
                full_key = f"{parent_key}_{key}" if parent_key else key
                full_value = f"{parent_key}_{key}_{value}" if parent_key else f"{key}_{value}"
                if parent_key.startswith('spec'): 
                  full_key = f"{kind}{parent_key}_{key}"
                  if isinstance(value, str):
                    if is_ip(value): # If the value is an IP, add it as "key_IP_value"
                        full_value = f"{full_key}_IP"
                    else:
                        full_value = f"{full_key}_{value}"
                # Search for the key in map2
                if full_key in map2:
                    feature = map2[full_key]
                    if feature not in keys:
                        keys.append(feature)
                        keys.extend(extract_keys(value, kind, full_key))
                    if full_value in map2:
                        feature = map2[full_value]
                        if feature not in keys:
                            keys.append(feature)
                            keys.extend(extract_keys(value, kind, full_key))
                # Search for the key in map1
                elif full_key in map1:
                    feature = map1[full_key]
                    if feature not in keys:
                        keys.append(feature)
                        keys.extend(extract_keys(value, kind, full_key))
                    if full_value in map1:
                        feature = map1[full_value]
                        if feature not in keys:
                            keys.append(feature)
                            keys.extend(extract_keys(value, kind, full_key))
    elif isinstance(yaml_content, list):
        full_key = f"{parent_key}"
        for item in yaml_content:
            if isinstance(item, str) and is_ip(item):
                keys.append(full_key + "_IP")
            keys.extend(extract_keys(item, kind, parent_key))
    return keys

# Obtain the group and version of the Kubernetes object.
def get_group_and_version(doc):
    var = doc.get('apiVersion', '').split('/')
    kind = doc.get('kind', '')
    if len(var) == 2:
        group, version = var
    else:
        group = 'core'
        version = var[0]
    return group, version, kind

# Count the keys in the YAML files.
def count_keys_in_folder(folder_path):
    key_counter = Counter()
    numConfPerManifest = {}
    for filename in tqdm(os.listdir(folder_path)):
        configs = 0
        if filename.endswith('.yaml'):
            file_path = os.path.join(folder_path, filename)
            try:
              with open(file_path, 'r', encoding='utf-8') as file:
                  documents = yaml.safe_load_all(file)
                  for doc in documents:
                      if doc is not None:
                          configs += 1
                          group, version, kind = get_group_and_version(doc)
                          keys = extract_keys(doc, kind.lower())
                          if kind in map1: keys.append(map1[kind])
                          if group in map1: keys.append(map1[group])
                          if version in map1: keys.append(map1[version])
                          key_counter.update(keys)
            except UnicodeDecodeError:
                #print(f"UnicodeDecodeError: Could not read {filename} with UTF-8 encoding. Trying with the default encoding.")
                try:
                    with open(file_path, 'r') as file:
                        documents = yaml.safe_load_all(file)
                        for doc in documents:
                            if doc is not None:
                                configs += 1
                                group, version, kind = get_group_and_version(doc)
                                keys = extract_keys(doc, kind)
                                if kind in map1: keys.append(map1[kind])
                                if group in map1: keys.append(map1[group])
                                if version in map1: keys.append(map1[version])
                                key_counter.update(keys)
                except (yaml.YAMLError, UnicodeDecodeError) as e:
                    continue
            except yaml.YAMLError as e:
                continue
            except AttributeError as e:
                #print(f"AttributeError: Could not read. {filename}.")
                continue
        numConfPerManifest[filename] = configs
    return key_counter, numConfPerManifest

# Add the mandatory child features that are not abstract
def add_mandatory_children(df, fm_model, feature, count, percentaje):
    for child in feature.get_children():
        if child.is_mandatory() and not child.is_abstract and child.name not in df['Feature'].values:
            df.loc[len(df)] = {'Feature': child.name, 'Count': count, 'Percentage': percentaje}
            for f in child.get_children():
                df = add_mandatory_children(df, fm_model, f, count, percentaje)
    return df

# Add the features that were not found in the YAML files and are not abstract
def add_features_not_found(df, fm_model):
    for feature in fm_model.get_features():
        if feature.name not in df['Feature'].values and not feature.is_abstract: # Only add non-abstract features
            df.loc[len(df)] = {'Feature': feature.name, 'Count': 0, 'Percentage': 0}
    return df

def main(folder_path, output_csv):
    fm_model = UVLReader(fm_file).transform() # Load the model
    create_mapping(mapping_file) # Create the 2 dictionaries to translate the YAML keys to features of the FM.
    key_counter, numConfPerManifest = count_keys_in_folder(folder_path) # Search for and count the features in the YAML files
    key_counts = key_counter.most_common() # Sort the features by frequency, from most common to least common
    
    df = pd.DataFrame(key_counts, columns=['Feature', 'Count']) # Create a DataFrame with the features and their frequency

    if not df.empty: # If the DataFrame is not empty, calculate the percentage of occurrences for each feature
        max_count = df['Count'].max()
        df['Percentage'] = (df['Count'] / max_count) * 100
        df['Percentage'] = df['Percentage'].round(4)  # Round to 4 decimal places

    try:
        for feature_name in df['Feature'].values:
            feature = fm_model.get_feature_by_name(feature_name)
            res = df.loc[df['Feature'] == feature.name, ['Count', 'Percentage']]
            count = int(res['Count'].values[0])        # Convert to integer
            percentaje = float(res['Percentage'].values[0])  # Convert to float
            df = add_mandatory_children(df, fm_model, feature, count, percentaje) # Add the mandatory child features
    except AttributeError as e:
        print(f"Error: Could not find the feature {feature_name} in the FM model.")

    df = add_features_not_found(df, fm_model) # Add the features that were not found in the YAML files

    df = df.sort_values(by='Count', ascending=False) # Sort the results by frequency

    # Save the number of configurations per manifest
    with open(output_numConfPerManifest_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['File', 'numConfigurations'])
        for key, value in numConfPerManifest.items():
            csv_writer.writerow([key, value])

    df.to_csv(output_csv, index=False)
    print(f"Results saved in {output_csv}.")

if __name__ == "__main__":
    main(folder_path, output_csv)