import json
import csv
import os
import pandas as pd

# Directory containing your JSON files
json_files_directory = "path/to_generalization_results"

# List to store extracted data
extracted_data = []

# Iterate through each JSON file in the directory
for filename in os.listdir(json_files_directory):
    if filename.endswith(".json"):
        with open(os.path.join(json_files_directory, filename), "r") as json_file:
            data = json.load(json_file)
            additional_statistics = data[-1].get("AdditionalStatistics", {})
            extracted_data.append(additional_statistics)
# print(extracted_data)


# Rows list initialization
rows = []

# Appending rows
for data in extracted_data:
    name = data['SketchMapLayerName']
    bm = data['NumberOfObjectsNotGeneralisedBaseMap']
    gbm = data['NumberOfObjectsGeneralisedBaseMap']
    align = data['NumberOfAlignedObjects']
    ng = data["NumberOfNoGeneralisations"]
    g = data["NumberOfGeneralisations"]
    r_ids= data["RepeatedAlignIDs"]
    t_ids = data["NoOfInstance"]
    non_A_ids= data ["Numberofnonalignedbaseids"]
    
    rows.append({'SketchMapLayerName': name, 'NumberOfObjectsBaseMap': bm, 'NumberOfObjectsGeneralisedBaseMap': gbm, 'NumberOfAlignedObjects': align, "NumberOfNoGeneralisations": ng, "NumberOfGeneralisations": g, "RepeatedAlignIDs": r_ids, "NoOfInstance": t_ids,"Numberofnonalignedbaseids": non_A_ids })

# Using DataFrame
df = pd.DataFrame(rows)

# # Print DataFrame
print(df)

# Define the CSV file path
csv_file_path = "path/testStatistics.csv"

# Write DataFrame to CSV
df.to_csv(csv_file_path, index=False, sep=';')

print("CSV file created:", csv_file_path)