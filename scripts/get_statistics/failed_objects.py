# Script that counts and groups invalid configurations by 'ObjectType' in a CSV file and saves the result in a text file.
# Useful for identifying which ones are failing and which to implement next.
# The functionality to count valid configurations by 'ObjectType' and save the result in a text file has been added.

import pandas as pd

# Load the file into a dataframe.
df = pd.read_csv('NonValidConfigs.csv')

# Count how many times each item appears in the "ObjectType" column
object_type_counts = df['ObjectType'].value_counts()

# Sort from highest to lowest (value_counts already returns the result sorted)
object_type_counts_sorted = object_type_counts.sort_values(ascending=False)

# Save the result in a text file.
with open('failed_objects.txt', 'w') as f:
    f.write(object_type_counts_sorted.to_string())

# Cargar el archivo en un dataframe
df = pd.read_csv(r'configurations/Configurations.csv')

# Count how many times each item appears in the "ObjectType" column
object_type_counts = df['ObjectType'].value_counts()

# Sort from highest to lowest (value_counts already returns the result sorted)
object_type_counts_sorted = object_type_counts.sort_values(ascending=False)

# Save the result in a text file.
with open('objects.txt', 'w') as f:
    f.write(object_type_counts_sorted.to_string())
