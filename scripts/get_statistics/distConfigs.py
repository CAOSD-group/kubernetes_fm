# Gets the number of valid, invalid, variability, and error configurations from a CSV file and saves the 
# configuration distribution based on the number of features in a CSV file. It also saves a CSV with the 
# failed configurations.

import csv
import pandas as pd

# Path of the CSV file
ruta_csv = r'configurations/Configurations.csv'

# Read the CSV file
df = pd.read_csv(ruta_csv)

# Count the valid configurations
configValidas = df[df['Valid'] == True].shape[0]

# Count the valid configurations (without variability) that have cardinality
configsValidasConCardinalidad = df[(df['Valid'] == True) & (df['ContainVariability'] == False) & (df['ContainCardinality'] == True)].shape[0]

# Count the valid configurations (without cardinality) that have variability
configValidasConVariabilidad = df[(df['Valid'] == True) & (df['ContainVariability'] == True) & (df['ContainCardinality'] == False)].shape[0]

# Count the invalid configurations (without errors).
configNoValidas = df[(df['Valid'] == False) & (df['ObjectType'] != 'none')].shape[0]
configNoValidasROWS = df[(df['Valid'] == False) & (df['ObjectType'] != 'none')]

# Count the invalid configurations (without errors) that have variability
configsNoValidasConVariabilidad = df[(df['Valid'] == False) & (df['ObjectType'] != 'none') & (df['ContainVariability'] == True)].shape[0]

# Count the configurations with errors.
configsErroneas = df[(df['ObjectType'] == 'none')].shape[0]

# Print the results.
print(f"Total valid configurations: {configValidas}")
print(f"Total valid configurations (without variability) with cardinality: {configsValidasConCardinalidad}")
print(f"Total valid configurations (without cardinality) with variability: {configValidasConVariabilidad}")
print(f"Total invalid configurations (without errors): {configNoValidas}")
print(f"Total invalid configurations (without errors) with variability: {configsNoValidasConVariabilidad}")
print(f"Total configurations with errors: {configsErroneas}")

# Calculate the total number of configurations
print(f"Total configurations read: {df.shape[0]}")

# Group by the number of 'numFeatures' and count (excluding configurations with variability or errors)
conteos_num_features = df[((df['ObjectType'] != 'none'))]['numFeatures'].value_counts().sort_index()


# Create an array or dictionary to store the distribution of configurations according to the number of numFeatures
resultados_num_features = {num: conteos_num_features.get(num, 0) for num in range(0, 735)} # 735 is the number of features in the model

# Save the results by the number of numFeatures
with open('distConfigs.csv', mode='w', newline='', encoding='utf-8') as csv_file:
  csv_writer = csv.writer(csv_file)
  csv_writer.writerow(['numFeatures', 'numConfigurations'])
  for num_features, count in resultados_num_features.items():
    csv_writer.writerow([num_features, count])

with open ('NonValidConfigs.csv', mode='w', encoding="utf-8") as csv_file:
  csv_writer = csv.writer(csv_file)
  csv_writer.writerow(configNoValidasROWS.columns)
  for index, row in configNoValidasROWS.iterrows():
    if row['ObjectType'] == "CustomResourceDefinition":
      continue
    else:
      csv_writer.writerow(row)