import os
import pandas as pd
import json

def transformJson(jsonData:dict):
    jsonData['action'] = jsonData['action'].keys()
    # try:
    #     jsonData['victim']['industry']['name'] = jsonData['attribute'].keys()
    return jsonData

def read_json_files(directory, limit=50):
    data_frames = []
    count = 0
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                data = transformJson(data)
                normalized_data = pd.json_normalize(data)
                data_frames.append(normalized_data)
                count += 1
                if count >= limit:
                    break
    return pd.concat(data_frames, ignore_index=True)

directory_path = 'C:/Users/sudharshan.acharya/Downloads/VCDB-master/VCDB-master/data/json/validated'
df = read_json_files(directory_path, limit=50)
columns_to_drop = ['incident_id', 'reference']
df = df.drop(columns=columns_to_drop)
print(df)
# print(df['action'])
# for column in df.columns:
#     print(column)
