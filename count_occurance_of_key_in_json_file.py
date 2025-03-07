import os
import json

def count_unique_values(directory, key):
    unique_values = set()

    for filename in os.listdir(directory):
        if filename.lower().endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                data = data['victim']
                if key in data:
                    unique_values.add(data[key])

    print(f"Number of unique values for key '{key}': {len(unique_values)}")
    print("Unique values:")
    for value in unique_values:
        # if value.isalpha():
        print(value)

# Example usage
directory = 'C:/Users/sudharshan.acharya/Downloads/VCDB-master/VCDB-master/data/json/validated'
key_to_check = 'industry'
count_unique_values(directory, key_to_check)