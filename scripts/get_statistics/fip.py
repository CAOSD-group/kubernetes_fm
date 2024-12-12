# This script creates a dictionary where the probabilities of each feature are stored and 
# then writes a CSV file with the percentages of the features grouped in 5% intervals.

import csv
import math

n_features = 0 # Total number of features in the input CSV. 
output_csv = 'FIP.csv' # Name of the output file.
source_csv = 'most_common_features.csv' # Name of the input file.
prob_dict = {} # Dictionary to store the probabilities of each feature.

# Read the input CSV file and store the probabilities of each feature in a dictionary.
def read_csv(source_csv):
  with open(source_csv, mode='r', encoding='utf-8') as file:
    reader_csv = csv.DictReader(file)
    for row in reader_csv:
      prob_dict[row["Feature"]] = float(row["Percentage"])
    n_features = prob_dict.__len__() 
    print(f"{n_features} features have been read.")
  return prob_dict, n_features


def write_csv(source_csv):
  INTERVALOS = 5
  DIFERENCIA = 0.025
  x_axis = [x/100.0 for x in range(0, 101, INTERVALOS)]
  count = [sum(math.isclose(x, round(p/100,2), abs_tol=DIFERENCIA) for p in prob_dict.values()) for x in x_axis]
  dead_features = sum(v/100 == 0.0 for v in prob_dict.values())
  count[1] = count[1] + (count[0] - dead_features)
  count[0] = dead_features
  core_features = sum(v/100 == 1.0 for v in prob_dict.values())
  count[-2] = count[-2] + (count[-1] - core_features)
  count[-1] = core_features

  y_axis = [round(c / n_features * 100, 2) for c in count]
  print(f'Count: {sum(count)}')
  with open(source_csv, mode='w', newline='', encoding='utf-8') as file:
    writer_csv = csv.writer(file)
    writer_csv.writerow(['Percentage', 'Features', 'Probability']) # Header
    for i in range(len(x_axis)):
      writer_csv.writerow([x_axis[i], count[i], y_axis[i]])


prob_dict, n_features = read_csv(source_csv)
write_csv(output_csv)
